# Overview
This project contains Python scripts for cleaning and transforming product review data. The script processes reviews by removing non-English entries, censoring profanity, normalizing ratings, and structuring the cleaned data with relevant product details such as name, image, brand, and reviews.

## Author 
Matthew Westerlund

## Files

- `clean_transform_data.py`: The main script that processes and cleans review data.

## Requirements

- Python 3.11+
- `langdetect`: For detecting the language of each review.
- `better-profanity`: For filtering out profanity.

## Setup Instructions

1. Install the required dependencies:
- `pip install langdetect better-profanity`
   
### Cleans and transforms review data.
* Removes non-English reviews and censors profanity.
* Normalizes star ratings from various formats (e.g., "4.5 out of 5 stars").
* Structures the cleaned reviews along with product metadata such as category, product name, image, unique key, and brand.

## Function
### clean_rate(x):
Extracts and normalizes the star rating from text input (e.g., "4.4 out of 5").
Handles potential errors when extracting ratings from strings.

## clean_transform_data(data)
Cleans and uniforms data strings from given data with the below categories, and iterates through the reviews to create usable data for the backend to use for the application


## Operation
data = {
    "Category": "Amazon",
    "Product Name": "Sample Product",
    "Product Image": "image_url",
    "Unique Key": "12345",
    "Clean URL": "sample_url",
    "Average Star": "4.5 out of 5 stars",
    "Brand": "Brand: Sample",
    "Reviews": [
        {"Review Text": "Great product!", "Date": "2023-09-10", "Stars": "5.0 out of 5"},
        {"Review Text": "Bad quality", "Date": "2023-09-08", "Stars": "1.0 out of 5"}
    ]
}
cleaned_data = clean_transform_data(data)

Notes
The script will skip reviews that are not in English.
Profane words in reviews will be censored using the better-profanity library.
The clean_rate() function ensures star ratings are consistently extracted and normalized.
Error Handling
Reviews without valid text or star ratings will be skipped.
If a review's language cannot be detected, it will be ignored.
The script ensures it proceeds with other reviews even when encountering errors during processing.