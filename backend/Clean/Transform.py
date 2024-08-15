import re
import json
import os
from langdetect import detect
from better_profanity import profanity
from datetime import datetime

# Initialize the better-profanity library
profanity.load_censor_words()

def convert_date(date_str):
    if date_str is None:
        raise ValueError("Date is None")
    
    # Remove any leading text before the actual date
    cleaned_date_str = re.sub(r'^.*on ', '', date_str)
    
    # Try to parse the cleaned date string with different formats
    for fmt in ('%d %B %Y', '%B %d %Y', '%B %d, %Y'):
        try:
            date_obj = datetime.strptime(cleaned_date_str, fmt)
            return date_obj #.strftime('%d %B %Y')
        except ValueError:
            pass
    
    raise ValueError(f'No valid date format found for {date_str}')


def clean_transform_data(data):
    cleaned_reviews = []
    
    # Extract product information
    product_name = data.get("Product Name", "")   
    product_image = data.get("Product Image", "")
    unique_key = data.get("Unique Key", "")
    brand = data.get("Brand", "")
    
    # Extract the reviews
    reviews = data.get("Reviews", [])

    for review in reviews:
        review_text = review.get('Review Text', '')
        review_date = review.get('Date', '')
        review_rating = review.get('Stars', '')

        # Remove Non-English reviews
        if detect(review_text) != 'en':
            continue

        # Filter out profanity
        review_text = profanity.censor(review_text)

        # Normalize text (handling Unicode)
        review_text = re.sub(r'[^\x00-\x7F]+', '', review_text)

        # Clean the date
        if review_date:
            try:
                review_date = convert_date(review_date)
                ##print(type(review_date))
            except ValueError as e:
                print(f"Error cleaning date: {e}")
                review_date = None
        else:
            review_date = None

        # Clean the rating
        if isinstance(review_rating, str):
            try:
                review_rating = float(re.findall(r'\d+\.\d+', review_rating)[0])
            except (ValueError, IndexError):
                review_rating = None
        elif isinstance(review_rating, float):
            # If it's already a float, we just pass
            pass
        else:
            review_rating = None

        cleaned_review = {
            'Review Text': review_text,
            'Date': review_date,
            'Stars': review_rating
        }
        cleaned_reviews.append(cleaned_review)
    
    # Return the complete data including product info and cleaned reviews
    return {
        'Product Name': product_name,
        'Product Image': product_image,
        'Unique Key': unique_key,
        'Brand': brand,
        'Reviews': cleaned_reviews
    }

# Example usage
##json_file_path = 'backend/Clean/amazon_product_details.json'

##with open(json_file_path, 'r', encoding='utf-8') as f:
    ##json_data = json.load(f)

##cleaned_data = clean_transform_data(json_data)

# If you want to save the cleaned data to a new file:
##output_file_path = 'backend/Clean/cleaned_amazon_product_details.json'
##with open(output_file_path, 'w', encoding='utf-8') as f:
    ##json.dump(cleaned_data, f, indent=4)
