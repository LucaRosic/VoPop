from airflow.decorators import dag, task
import datetime as dt
import sqlite3
import sys
import requests
sys.path.insert(1, '/Users/noahpalmer/Documents/FDM/Cassowary/VoPop/VoPop/backend/Clean/')
from Transform import clean_transform_data
sys.path.insert(1, '/Users/noahpalmer/Documents/FDM/Cassowary/VoPop/VoPop/backend/ML/')
from sentiment import start_model,analyseSentiment
    
# @dag(
# schedule='@daily',
# start_date=dt.datetime(2024,1,1),
# catchup=False,
# dag_id='update_reviews'
# )
def get_latest_reviews():

    connection = sqlite3.connect("backend/db.sqlite3")
    cursor = connection.cursor()

    #@task(task_id='retrieve_urls')
    def retrieve_outdated_urls():
        
        result = cursor.execute("SELECT url,date,product_id from api_product_summary ps JOIN api_product p ON ps.product_id = p.id LIMIT 1")
        return result.fetchall()

    #@task(task_id='scrape')
    def scrape_new_data(product_list):
        new_reviews ={}
        for url, date, product_id in product_list:
            if dt.datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f") < dt.datetime.now(): #- dt.timedelta(days=31):
               payload = {'url':url,'date':date}
               fresh_reviews = requests.get('http://localhost:8000/api/product/newreviews/', params=payload)
               new_reviews[product_id] = fresh_reviews
        return new_reviews
    
    #@task(task_id='transform')
    def transform_new_data(new_data):
        return clean_transform_data(new_data)
    
    #@task(task_id='analyse_sentiment')
    def analyse_review_sentiment(reviews):
        
        for review in reviews['Reviews']:
                
            # Sentiment
            sent_model = start_model()
            sentiment = analyseSentiment(sent_model, review['Review Text'])
            cursor.execute(f"INSERT INTO api_product_reviews (review,sentiment,sentiment_label,rating,date,product_id) VALUES ({new_data['review']},{new_data['score']},{new_data['label']},{new_data['Stars']},{new_data['Date']},{new_data['review']},)")

        cursor.close()
                
        return None
    
    #@task(task_id='update_product_review_database')
    def update_review_database(new_data):
        #for review in new_data:
            
            return None

    old_urls = retrieve_outdated_urls()
    new_data = scrape_new_data(old_urls)
    transformed_data = transform_new_data(new_data)
    new_sentiment = analyse_review_sentiment(transformed_data)
    update_review_database(new_sentiment)

get_latest_reviews()

if __name__ == "__main__":
    get_latest_reviews()