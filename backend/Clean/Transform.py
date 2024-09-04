import re
import json
import os
import sys
from langdetect import detect
from better_profanity import profanity
from datetime import datetime
# from ..scrape.scrapper import scrape_reviews

# Initialize the better-profanity library
profanity.load_censor_words()

# def convert_date(date_str):
#     if date_str is None:
#         raise ValueError("Date is None")
    
#     # Check if the date string contains a '|' and extract the part after it
#     if '|' in date_str:
#         cleaned_date_str = date_str.split('|')[1].strip()
#     else:
#         # Remove any leading text before the actual date using "on" as a reference point
#         cleaned_date_str = re.sub(r'^.*on\s+', '', date_str).strip()
#     print(cleaned_date_str)
    
#     # Try to parse the cleaned date string with different formats
#     for fmt in ('%d %B %Y', '%B %d %Y', '%B %d, %Y','%d %b %Y'):
#         try:
#             date_obj = datetime.strptime(cleaned_date_str, fmt)
#             return date_obj .strftime('%d %B %Y')
#         except ValueError:
#             pass
    
#     raise ValueError(f'No valid date format found for {date_str}')


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

    if "Brand: " in brand:
        brand=brand.split(":",1)[1].strip()
    
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

        # # Clean the date
        # if review_date:
        #     try:
        #         review_date = convert_date(review_date)
        #         ##print(type(review_date))
        #     except ValueError as e:
        #         print(f"Error cleaning date: {e}")
        #         review_date = None

        
    
        
        
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

json_file_path = 'backend/Clean/amazon_product_details.json'

# if __name__ == "__main__":
#     url='https://amazon.com.au/Wireless-Mechanical-Keyboard-Bluetooth-Swappable/dp/B0D1XKDWFM/ref=sr_1_6?crid=2O0NHFPX8TPWO&dib=eyJ2IjoiMSJ9.KEZMeBqM8DaV6pqo_GHgPkvI4g0GL2Dn0psNSqinazgW1JJTR6ZNVybpJKS4sapTORB5PVPvmsylhA22pDq-A0lZpVqVwM-wKmzeozI_oBaKcU9OBwOoJJ3NJEnx2m8hDNI-5OLY-ZIqLyA0C8BEQMYiLbaKf7ERZuWPQPkeMj0ktsV3d1DvtE9bNBRLbQtgj-9vxGDdC5dXcHcLQXJ6sADRjKCHeiPp4HzsHDhR8Zsf8Dg3HEfmqwRfgrTBC-9eTKNAuHocnw8FR98a1yQQ2vEmbE9Q7EiCP0YC7zV6OKU.6n0CW1fFTGvuG5wSKHgYOTKYEpUd7wV1_V1kfPzIZsw&dib_tag=se&keywords=b87+keyboard&qid=1724629811&sprefix=b87%2Caps%2C252&sr=8-6'
#     date = datetime(day=2,month=7, year=2024)
#     reviews_df = clean_transform_data(scrape_reviews(url,date))
#     print('end')