# Overview
This project contains Python scripts that uses Selenium to scrape product reviews from Amazon and AliExpress. The code extracts product details such as the product name, image, average star rating, brand, and user reviews, including the date and rating of each review.

## Files

scrapper.py: The main script containing functions to scrape reviews from Amazon and AliExpress.
GeckoDriver: Driver to simulate and automate the scrape function

## Requirements
Python 3.11+
Selenium
Firefox WebDriver (GeckoDriver)


## Setup Instructions
From the backend folder ensure prior requirements.txt has been pip installed 

## Install the required dependencies:
pip install -r requirements.txt

Download the GeckoDriver for Firefox and provide the path to gecko_driver_path in the script:
https://github.com/mozilla/geckodriver/releases/download/.....


### Functions

scrape_reviews(url, date_filter=None):
Scrapes reviews from Amazon, including product name, image, average rating, brand, and reviews.
Optionally filters reviews based on a provided date.

If a date is added in a dateobj format (d% B% Y%) and the product has been previously been processed the scraper will only grab latest information post date provided
NOTE: this date function is purely for backend and airflow updating product measures, no one should have direct access to this functionality 

### verification 

when scrape_reviews() is called it goes through the following functions to ensure valid amazon or AliExpress links have been provided and process the correct scraper 

is_valid_url(url): Function to validate the URL structure.
get_site(url): Determines if the URL is for Amazon or AliExpress.
clean_url(url): Cleans and simplifies the product URL for easier processing.
convert_date(date_str): Converts various date formats into a standardized format.

scrape_ali_express_reviews(url):
Scrapes reviews from AliExpress, including product name, image, average rating, and reviews.
Usage


## To run the scraper:

Set the URL of the product to scrape (Amazon or AliExpress).
Call the appropriate function:
python
date = datetime(day=15,month=7, year=2024)
scrape_reviews("https://www.amazon.com/product-reviews/...")
scrape_reviews("https://www.aliexpress.com/item/...",date)


### Notes
Make sure the GeckoDriver path is correctly set in the script.
The script is currently designed to run in headless mode for performance. To enable browser visibility, comment out --headless in the options.
If scraping AliExpress, the script may need further customization for infinite scrolling and loading additional reviews.
Error Handling
The script includes basic error handling for missing elements and page load issues.
If issues arise with product information extraction, the script will skip the missing data and continue scraping reviews.