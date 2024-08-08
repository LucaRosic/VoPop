import re
import json
import os
from langdetect import detect
from better_profanity import profanity

# Initialize the better-profanity library
profanity.load_censor_words()

def clean_transform_data(data):
    cleaned_reviews = []
    
    # Extract product information
    product_name = data.get("Product Name", "")
    product_image = data.get("Product Image", "")
    unique_key = data.get("Unique Key", "")
    brand = data.get("Brand", "")
    
    
    # Extract the reviews
    reviews = data.get("Reviews", [])  # Access the list of reviews

    for review in reviews:
        review_text = review.get('Review Text', '')  # Access review text with a default empty string
        review_date = review.get('Date', '')  # Access review date with a default empty string
        review_rating = review.get('Stars', '')  # Access review rating with a default empty string

        # Remove Non-English reviews
        if detect(review_text) != 'en':
            continue

        # Filter out profanity
        review_text = profanity.censor(review_text)

        # Normalize text (handling Unicode)
        review_text = re.sub(r'[^\x00-\x7F]+', '', review_text)

        # Clean the date
        date_match = re.search(r'on (\d{1,2}) (\w+) (\d{4})', review_date)
        if date_match:
            day, month_str, year = date_match.groups()
            month = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }.get(month_str, None)
            if month:
                review_date = [int(day),int(month),int(year)]  
            else:
                review_date = None  # Handle cases where month is not valid
        else:
            review_date = None  # Handle cases where date is not in the expected format

        # Clean the rating
        try:
            review_rating = float(re.findall(r'\d+\.\d+', review_rating)[0])
        except (ValueError, IndexError):
            review_rating = None  # Handle cases where rating is not a valid float

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


if __name__ == '__main__':
    # Path to the directory containing JSON files
    directory = "Input_Data/"
    output_directory = "Output_Data/"

    # Process each JSON file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                print(clean_transform_data(data))