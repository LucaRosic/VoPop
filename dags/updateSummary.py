from airflow.decorators import dag, task
import datetime as dt
import sqlite3
import sys

@dag(
schedule='@daily',
start_date=dt.datetime(2024,1,1),
catchup=False,
dag_id='update_review_summary'
)
def update_review_summary():
    
    @task(task_id='get_reviews')
    def get_reviews():
        return None

    @task(task_id='update_summary')
    def update_product_summary(reviews):
        return None
    
    @task(task_id='update_product_summary_database')
    def update_ps_database(new_summary):
        return None

    reviews = get_reviews()
    new_summary = update_product_summary(reviews)
    update_ps_database(new_summary)

update_review_summary()