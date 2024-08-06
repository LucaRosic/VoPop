import pandas as pd
import json
import re
from profanity_check import predict
from textblob import TextBlob
import unicodedata
from langdetect import detect
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

# Django settings
import django
django.setup()

# Define Django models 
class Review(models.Model):
    review_text = models.TextField()
    date = models.DateTimeField()
    stars = models.IntegerField()

def clean_review_text(text):
    # Filter out profanity
    text = text if not predict([text])[0] else TextBlob(text).words
    # Correct spelling and grammar
    text = str(TextBlob(text).correct())
    # Normalize text (handling Unicode)
    text = unicodedata.normalize('NFKD', text).encode('ascii', errors='ignore').decode('utf-8')
    # Identify and remove noise
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def clean_reviews():
    # Fetch reviews from the database
    reviews = Review.objects.all()
    
    # Create a DataFrame
    df = pd.DataFrame(list(reviews.values('id', 'review_text', 'date', 'stars')))
    
    # Drop null values
    df = df.dropna()
    
    # Clean and transform review text
    df['cleaned_text'] = df['review_text'].apply(clean_review_text)
    
    # Remove non-English reviews
    df = df[df['cleaned_text'].apply(lambda x: detect(x) == 'en')]
    
    # Update the original data with cleaned reviews
    cleaned_reviews = df[['id', 'date', 'stars', 'cleaned_text']].rename(columns={'cleaned_text': 'review_text'})
    
    # Save cleaned data back to the database
    for _, row in cleaned_reviews.iterrows():
        try:
            review = Review.objects.get(id=row['id'])
            review.review_text = row['review_text']
            review.save()
        except ObjectDoesNotExist:
            pass  # Handle if the review ID no longer exists

# Call the function
clean_reviews()
