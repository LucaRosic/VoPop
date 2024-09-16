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
        tablenames = cursor.execute("SELECT table_name FROM information_schema.tables;")
        print(tablenames)
        result = cursor.execute("SELECT url,date,product_id FROM product_summary ps JOIN roduct p ON ps.product_id = p.id")
        return result.fetchall()
    
    #check if last summary date older than a month. If yes, scrape new reviews using backend api.
    @task(task_id='scrape')
    def scrape_new_data(product_list):
        
        new_reviews ={}
        for url, date, product_id in product_list:
     
            if dt.datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f") < dt.datetime.now(): #- dt.timedelta(days=31):
               payload = {'url':url,'date':str(date.split()[0])}
               fresh_reviews = requests.get('http://host.docker.internal:8000/api/product/newreviews/', params=payload)
               new_reviews[product_id] = fresh_reviews.text
             
        return new_reviews

    #Format data to be ready for insertion into database. Sentiment analysis done using api call. Could optimise.
    @task(task_id='transform')
    def transform_new_data(new_data):
        
        profanity.load_censor_words()
        cleaned_reviews = []
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
                
                if review_rating:
                    review_rating = clean_rate(review_rating)
                # Sentiment
                sentiment = json.loads(requests.get('http://host.docker.internal:8000/api/product/newsentiment/',{'review':review_text}).text)
                
                cleaned_review = {
                    'Date': review_date.split('T')[0],
                    'Stars': review_rating,
                    'Review Text': review_text.replace('"',"'").replace(',','').replace("'",''),
                    'Sentiment': sentiment['label'],
                    'Score': sentiment['score'],
                    'prod_id': id
                }
                cleaned_reviews.append(cleaned_review)

             
        return cleaned_reviews
    
    #insert new reviews into db
    @task(task_id='update_review_db')
    def update_review_database(new_data):
        for review in new_data:
         
            cursor.execute(f"INSERT INTO api_product_reviews (review, sentiment, sentiment_label, rating,date, product_id) VALUES ('{review['Review Text']}',{review['Score']},'{review['Sentiment']}',{review['Stars']},'{review['Date']}',{review['prod_id']});")
            connection.commit()
        #cursor.close()    
        return None
    
    #call gemini api to generate new summary, then update database.
    @task(task_id='update_summary')
    def update_review_summary(old_product):
        for url, date, product_id in old_product:
            
            result = cursor.execute(f"SELECT review FROM api_product_reviews WHERE product_id={product_id}").fetchall()

            new_summaries = []
            for review in result:
                 new_summaries.append({"Review Text":review[0]})
            summary = summarize(new_summaries).replace('"',"").replace("'","")
         
            cursor.execute(f"UPDATE api_product_summary SET summary = '{summary}' WHERE product_id = {product_id}" )
            cursor.execute(f"UPDATE api_product_summary SET date = '{dt.datetime.now()}' WHERE product_id = {product_id}" )
            connection.commit()
        cursor.close()
        return summary

    #DAG dependency structure
    old_urls = retrieve_outdated_urls()
    print(old_urls)
    new_data = scrape_new_data(old_urls)
    transformed_data = transform_new_data(new_data)
    update_review_database(transformed_data) >> update_review_summary(old_urls)

get_latest_reviews()

if __name__ == "__main__":
    get_latest_reviews()