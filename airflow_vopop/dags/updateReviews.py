from airflow.decorators import dag, task
import datetime as dt
import sqlite3
import sys
import requests
import json
from langdetect import detect
from better_profanity import profanity
import re
import os
import psycopg2
import pytz
os.environ['NO_PROXY'] = '*'

#need to fix imports
#sys.path.insert(1, '/Users/noahpalmer/Documents/FDM/Cassowary/VoPop/VoPop/backend/ML/')
from ReviewSumModel import summarize

def clean_rate(x):
            if isinstance(x, str):
                try:
                    # Extract the first floating point number found in the string
                    x = float(re.findall(r'\d+\.\d+', x)[0])
                    print(x)
                except (ValueError, IndexError):
                    x = None
            elif isinstance(x, float):
                # If it's already a float, we just pass
                pass
            else:
                x = None
            
            return x


@dag(
schedule='@daily',
start_date=dt.datetime(2024,1,1),
catchup=False,
dag_id='update_reviews'
)
def get_latest_reviews():

    #adjust db connection
    connection = psycopg2.connect(database="airflow", user='airflow', password='airflow', host='host.docker.internal', port= '5432')
    cursor = connection.cursor()

    #get urls and summary dates for each product
    @task(task_id='retrieve_urls')
    def retrieve_outdated_urls():
        
        cursor.execute("SELECT pds.source as url,ps.date,ps.product_id,pds.unique_code\
                        FROM api_product_summary ps\
                        JOIN api_product p ON ps.product_id = p.id\
                        JOIN api_product_data_source pds ON p.id = pds.product_id\
                        WHERE date < date_trunc('day', NOW() - interval '1 day')")
        return cursor.fetchall()
    
    #check if last summary date older than a month. If yes, scrape new reviews using backend api.
    @task(task_id='scrape')
    def scrape_new_data(product_list):
        
        new_reviews ={}
        for url, date, product_id, unique_code in product_list:
            # utc=pytz.UTC
            # datenow= utc.localize(dt.datetime.now())
            # #challenge.datetime_end = utc.localize(challenge.datetime_end)
            # if date < datenow - dt.timedelta(days=31):
            payload = {'url':url,'date':date.strftime('%Y-%m-%d')}
            fresh_reviews = requests.get('http://host.docker.internal:8000/api/product/newreviews/', params=payload)
            new_reviews[unique_code] = fresh_reviews.text
             
        return new_reviews

    #Format data to be ready for insertion into database. Sentiment analysis done using api call. Could optimise.
    @task(task_id='transform')
    def transform_new_data(new_data):
        
        profanity.load_censor_words()
        cleaned_reviews = []
        texts = []
        for id in new_data.keys():
            for review in json.loads(new_data[id]):
                
                review_text = review.get('Review Text', '')
                review_date = review.get('Date', '')
                review_rating = review.get('Stars', '')

                try:# Remove Non-English reviews
                    if detect(review_text) != 'en':
                        print('not good')
                        continue
                except:
                    print("this shit borken")
                    continue

                # Filter out profanity
                review_text = profanity.censor(review_text)
                texts.append(review_text.replace('"',"").replace(',','').replace("'",''))
                if review_rating:
                    review_rating = clean_rate(review_rating)
                
                
                cleaned_review = {
                    'Date': review_date.split('T')[0],
                    'Stars': review_rating,
                    'Review Text': review_text.replace('"',"'").replace(',','').replace("'",''),
                    'Sentiment': None, #sentiment['label'],
                    'Score': None, #sentiment['score'],
                    'prod_id': id
                }
                cleaned_reviews.append(cleaned_review)


        # Sentiment
        sentiment = json.loads(requests.post('http://host.docker.internal:8000/api/product/newsentiment/',{'review':texts}).text)
        i=0
        sentiment_reviews = []
        for review in cleaned_reviews:
            review['Sentiment'] = sentiment[str(i)]['label']
            review['Score'] = sentiment[str(i)]['score']
            i+=1
            sentiment_reviews.append(review)
        return sentiment_reviews
    
    #insert new reviews into db
    @task(task_id='update_review_db')
    def update_review_database(new_data):
        for review in new_data:
         
            cursor.execute(f"""INSERT INTO api_product_reviews (review, sentiment, sentiment_label, rating,date, unique_code) VALUES ('{review['Review Text']}',{review['Score']},'{review['Sentiment']}',{review['Stars']},'{review['Date']}',{review['prod_id']});""")
            connection.commit()
        #cursor.close()    
        return None
    
    #call gemini api to generate new summary, then update database.
    @task(task_id='update_summary')
    def update_review_summary(old_product):

        updated_id = []

        for url, date, product_id, unique_code in old_product:
            if product_id not in updated_id:
                cursor.execute(f"SELECT review FROM api_product_reviews WHERE unique_code in (SELECT pds.unique_code FROM api_product_summary ps JOIN api_product p ON ps.product_id = p.id JOIN api_product_data_source pds ON p.id = pds.product_id WHERE pds.product_id ={product_id} )")

                new_summaries = []
                for review in cursor.fetchall():
                    new_summaries.append({"Review Text":review[0]})
                summary = summarize(new_summaries).replace('"',"").replace("'","")
                updated_id.append(product_id)
                cursor.execute(f"""UPDATE api_product_summary SET summary = '{summary}',date = '{dt.datetime.now()}' WHERE product_id = {product_id}""" )
                #cursor.execute(f"UPDATE api_product_summary SET  WHERE product_id = {product_id}" )
                connection.commit()
        cursor.close()
        connection.close()
        return summary

    #DAG dependency structure
    old_urls = retrieve_outdated_urls()
    print(old_urls)
    new_data = scrape_new_data(old_urls)
    transformed_data = transform_new_data(new_data)
    update_review_database(transformed_data) >> update_review_summary(old_urls)

get_latest_reviews()

#if __name__ == "__main__":
#    get_latest_reviews()