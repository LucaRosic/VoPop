# This is to compare sentiment models time taken and score
# Have to run this file from the ML folder

# Supress future warnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import sys
sys.path.insert(1, '../Clean')
sys.path.insert(1, '../scrape')
from Transform import clean_transform_data
from scrapper import scrape_reviews
from sentiment import analyseSentiment, start_model
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from datetime import datetime
import functools # For the reduce function
import statistics
# >> python -m spacy download en_core_web_sm


# url_to_scrape = input("Enter URL: ")
url_to_scrape = r"https://www.amazon.com/Kindle-Paperwhite-Signature-including-Lockscreen/dp/B0BN4ZLQR2/ref=sr_1_1?sr=8-1"
scraped = (scrape_reviews(url_to_scrape))
cleaned = clean_transform_data(scraped)

print()
print("BERT sentiment test commencing...")

start_bert = datetime.now()

postive_count = 0
negative_count = 0
sent_model = start_model()

for review in cleaned['Reviews']:
                
    # Sentiment
    sentiment = analyseSentiment(sent_model, review['Review Text'])
    
    # Count positive and negative reviews
    if sentiment['label'] == 'Positive':
        postive_count += 1
    elif sentiment['label'] == 'Negative':
        negative_count += 1

 # Calculate avg. sentiment (NPS) for Product       
nps_bert = round( (postive_count/len(cleaned['Reviews'])) - (negative_count/len(cleaned['Reviews']) ) ,2)

end_bert = datetime.now()
print("Bert sentiment finished!")


print()
print("Spacy sentiment test commencing...")

start_spacy = datetime.now()

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")

sentiment_polarity = []
for review in cleaned["Reviews"]:
    docx = nlp(review['Review Text'])
    sentiment_polarity.append(docx._.polarity)

total_reviews = len(cleaned["Reviews"])
num_positive = functools.reduce(lambda x,y: x+1 if y > 0 else x, sentiment_polarity, 0)
num_negative = functools.reduce(lambda x,y: x+y if y < 0 else x, sentiment_polarity, 0)

promoters = functools.reduce(lambda x,y: x+1 if y > 0.4 else x, sentiment_polarity, 0) # Give threshold for promoters
detractors = functools.reduce(lambda x,y: x+y if y < -0.1 else x, sentiment_polarity, 0) # Give threshold for detractors

nps_spacy_naive = round((num_positive/total_reviews) - (num_negative/total_reviews), 2)
nps_spacy = round((promoters/total_reviews) - (detractors/total_reviews), 2)

avg_polarity = statistics.mean(sentiment_polarity)

end_spacy = datetime.now()
print("Spacy sentiment finished!")

print()
print("===== Results =====")

print()
print("--- BERT ---")
print(f"Time: {(end_bert-start_bert).total_seconds()}s  ||  NPS: {nps_bert}")

print()
print("--- Spacy ---")
print(f"Time: {(end_spacy-start_spacy).total_seconds()}s  ||  NPS (naive): {nps_spacy_naive}")
print(f"Time: {(end_spacy-start_spacy).total_seconds()}s  ||  NPS (thresholded): {nps_spacy}")
print(f"Average polarity: {avg_polarity}")