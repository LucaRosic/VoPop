import os
import json
import pandas as pd
from langdetect import detect
from better_profanity import profanity
from textblob import TextBlob
import re

# import sqlalchemy
# from sqlalchemy import create_engine
import psycopg2



# Initialize the better-profanity library
profanity.load_censor_words()

# Define a function to clean and transform the data
def clean_transform_data(reviews):
    
    # Remove duplicates
    reviews = reviews.drop_duplicates(subset=['review'])

    # Remove Non-English reviews
    reviews = reviews[reviews['cleaned_text'].apply(lambda x: detect(x) == 'en')]

    # Filter out profanity
    reviews['cleaned_text'] = reviews['review'].apply(lambda x: profanity.censor(x))

    # Correct spelling and grammar
    reviews['cleaned_text'] = reviews['cleaned_text'].apply(lambda x: str(TextBlob(x).correct()))

    # Normalize text (handling Unicode)
    reviews['cleaned_text'] = reviews['cleaned_text'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    # Identify and remove noise
    reviews['cleaned_text'] = reviews['cleaned_text'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))

    return reviews

# Function to load data into the PostgreSQL database
def load_to_db(df, db_engine, table_name):
    df.to_sql(table_name, db_engine, if_exists='append', index=False)



# Set up PostgreSQL database connection
db_username = 'your_username'
db_password = 'your_password'
db_host = 'localhost'
db_port = '5432'
db_name = 'your_database'
engine = create_engine(f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
table_name = 'your_table'

# Path to the directory containing JSON files
directory = '/path/to/dir/of/json/files'

# Process each JSON file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:

            data = json.load(file)
            df = pd.DataFrame(data)
            cleaned_df = clean_transform_data(df)
            load_to_db(cleaned_df, engine, table_name)


