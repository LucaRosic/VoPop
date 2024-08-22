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
    
    # Check if the date string contains a '|' and extract the part after it
    if '|' in date_str:
        cleaned_date_str = date_str.split('|')[1].strip()
    else:
        # Remove any leading text before the actual date using "on" as a reference point
        cleaned_date_str = re.sub(r'^.*on\s+', '', date_str).strip()
    print(cleaned_date_str)
    
    # Try to parse the cleaned date string with different formats
    for fmt in ('%d %B %Y', '%B %d %Y', '%B %d, %Y','%d %b %Y'):
        try:
            date_obj = datetime.strptime(cleaned_date_str, fmt)
            return date_obj .strftime('%d %B %Y')
        except ValueError:
            pass
    
    raise ValueError(f'No valid date format found for {date_str}')


def clean_transform_data(data):
    cleaned_reviews = []

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
    
    # Extract product information
    category = data.get("Category","")
    product_name = data.get("Product Name", "")   
    product_image = data.get("Product Image", "")
    unique_key = data.get("Unique Key", "")
    clean_url = data.get("Clean URL","")
    avg_star = data.get("Average Star","")
    brand = data.get("Brand", "")
    
    # Extract the reviews
    reviews = data.get("Reviews", [])

    for review in reviews:
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

        # Clean the date
        if review_date:
            try:
                review_date = convert_date(review_date)
                ##print(type(review_date))
            except ValueError as e:
                print(f"Error cleaning date: {e}")
                review_date = None

        
    
        
        
        if review_rating:
            review_rating = clean_rate(review_rating)
        if category == 'Amazon':
            avg_star = clean_rate(avg_star)


        cleaned_review = {
            'Date': review_date,
            'Stars': review_rating,
            'Review Text': review_text
        }
        cleaned_reviews.append(cleaned_review)
    
    # Return the complete data including product info and cleaned reviews
    return {
        'Category': category,
        'Product Name': product_name,
        'Product Image': product_image,
        'Unique Key': unique_key,
        'Clean URL': clean_url,
        'Brand': brand,
        'Average Stars': avg_star,
        'Reviews': cleaned_reviews
    }

json_file_path = 'backend/Clean/aliexpress_product_details.json'

with open(json_file_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

cleaned_data = clean_transform_data(json_data)

# If you want to save the cleaned data to a new file:
output_file_path = 'backend/Clean/cleaned_amazon_product_details.json'
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, indent=4)
