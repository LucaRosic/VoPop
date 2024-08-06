from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from urllib.parse import urlparse
import json
from selenium import webdriver

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_site(url):
    if 'amazon' in url:
        return 'amazon'
    elif 'etsy' in url:
        return 'etsy'
    elif 'alibaba' in url:
        return 'alibaba'
    else:
        return None

def scrape_amazon_reviews(url):
    count=0
    def clean_url(url):
        if "/product-reviews/" in url:
            url = url.replace("/product-reviews/", "/dp/")
        elif "/dp/" in url:
            parts = url.split("/dp/")
            if "/ref" in parts[1]:
                clean_part = parts[1].split("/ref")[0]
            else:
                clean_part = parts[1].split("?")[0]
            url = parts[0] + "/dp/" + clean_part, clean_part
        return url 
        
    

    print("Amazon detected")
    start_time = time.time()

    # Specify the path to your GeckoDriver executable
    gecko_driver_path = r'backend\scrape\geckodriver.exe'

    # Configure Firefox options
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    # Initialize FirefoxDriver service
    service = Service(gecko_driver_path)

    # Initialize Firefox WebDriver with service and options
    driver = webdriver.Firefox(service=service, options=options)

    # Clean the URL
    cleaned_url, unique_key = clean_url(url)
    driver.get(cleaned_url)

    # Initialize an empty list to store reviews
    reviews_list = []

    try:
        # Scrape product details
        product_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'productTitle'))
        ).text

        product_image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'landingImage'))
        ).get_attribute('src')

        # Click on the "See more reviews" link if present
        try:
            see_more_reviews = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-hook="see-all-reviews-link-foot"]'))
            )
            see_more_reviews.click()
        except Exception as e:
            print("See more reviews link not found or error:", e)

        while True:
            # Extract review elements
            review_elements = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.a-section.review'))
            )

            # Iterate over each review element
            for review in review_elements:
                
                try:
                    # Extract review text
                    review_text = review.find_element(By.CSS_SELECTOR, '.review-text-content').text
                    # Extract review date
                    review_date = review.find_element(By.CSS_SELECTOR, '.review-date').text
                    # Extract star rating
                    review_stars = review.find_element(By.CSS_SELECTOR, '.a-icon-alt').get_attribute('textContent')
                    count+=1
                    # Append the extracted data to the reviews list
                    reviews_list.append({
                        'Date': review_date,
                        'Stars': review_stars,
                        'Review Text': review_text
                    })
                    
                except Exception as e:
                    print("Error extracting review details:", e)

            # Check for the "Next page" link and click if found
            try:
                next_page = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#cm_cr-pagination_bar > ul > li.a-last > a'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_page)  # Ensure element is in view
                next_page.click()
                WebDriverWait(driver, 3).until(
                    EC.invisibility_of_element((By.CSS_SELECTOR, 'div.a-section.cr-list-loading.reviews-loading'))
                )  # Wait for loading overlay to disappear
            except Exception as e:
                print(count)
                print("No more pages or error navigating to next page:", e)
                break

    finally:
        # Close the WebDriver
        driver.quit()

    # # Create a DataFrame from the reviews list
    # df = pd.DataFrame(reviews_list)

    # # Save the reviews DataFrame as a JSON file
    # df.to_json('amazon_reviews.json', orient='records', lines=True)

    # Create a product details dictionary
    product_details = {
        'Product Name': product_name,
        'Product Image': product_image,
        'Unique Key': unique_key,
        'Reviews': reviews_list
    }

    # Save product details as a JSON file
    with open('amazon_product_details.json', 'w') as file:
        json.dump(product_details, file, indent=4)

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Scraping completed in {elapsed_time:.2f} seconds")

    return product_details



def scrape_etsy_reviews(url):
    print("Etsy detected")
    # Specify the path to your GeckoDriver executable
    gecko_driver_path = r'C:\Users\Matth\OneDrive\Documents\FDM training\pond\dashboard_project\geckodriver.exe'

    # Configure Firefox options
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')

    # Initialize FirefoxDriver service
    service = Service(gecko_driver_path)

    # Initialize Firefox WebDriver with service and options
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)

    # Initialize an empty list to store reviews
    reviews_list = []

    try:
        while True:
            # Extract review elements
            review_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.review'))
            )

            # Iterate over each review element
            for review in review_elements:
                try:
                    # Extract review text
                    review_text = review.find_element(By.CSS_SELECTOR, '.review-text').text
                    # Extract review date
                    review_date = review.find_element(By.CSS_SELECTOR, '.review-date').text
                    # Extract star rating
                    review_stars = review.find_element(By.CSS_SELECTOR, '.star-rating').get_attribute('textContent')

                    # Append the extracted data to the reviews list
                    reviews_list.append({
                        'Date': review_date,
                        'Stars': review_stars,
                        'Review Text': review_text
                    })
                except Exception as e:
                    print("Error extracting review details:", e)

            # Check for the "Next page" link and click if found
            try:
                next_page = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.pagination-next'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_page)  # Ensure element is in view
                next_page.click()
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element((By.CSS_SELECTOR, 'div.a-section.cr-list-loading.reviews-loading'))
                )  # Wait for loading overlay to disappear
            except Exception as e:
                print("No more pages or error navigating to next page:", e)
                break

    finally:
        # Add a delay before quitting to inspect any error messages
        time.sleep(10)
        
        # Close the WebDriver
        driver.quit()

    # Create a DataFrame from the reviews list
    df = pd.DataFrame(reviews_list)

    # Save the DataFrame as a JSON file
    df.to_json('etsy_reviews.json', orient='records', lines=True)

    return df

def scrape_ali_express_reviews(url):
    print("AliExpress detected")
    # Implement Alibaba scraping herev
    pass

def scrape_reviews(url):
    if not is_valid_url(url):
        print("Invalid URL")
        return None

    site = get_site(url)
    if site == 'amazon':
        return scrape_amazon_reviews(url)
    elif site == 'etsy':
        return scrape_etsy_reviews(url)
    elif site == 'aliexpress':
        return scrape_ali_express_reviews(url)
    else:
        print("Unsupported site")
        return None

# Example usage
if __name__ == "__main__":
    # url = "https://www.etsy.com/au/listing/1518307138/personalized-travel-jewelry-box-small?click_key=e840c0f4cb9842b5b33c7993184a9c63c837c426%3A1518307138&click_sum=dd8b8e24&ref=hp_prn-1&pro=1&sts=1"
    # url = "https://www.alibaba.com/product-detail/2020-Innovation-Smart-Watch-Band-Fitness_62471952214.html?spm=a27aq.27039648.4955574140.39.19db3ccf02rzO0 "
    url = 'https://www.amazon.com.au/Lip-Smacker-Coca-Cola-Party-Glosses/dp/B00CXK623E/?_encoding=UTF8&pd_rd_w=2LQ0T&content-id=amzn1.sym.619da892-3961-430f-af2a-2290db51abf0&pf_rd_p=619da892-3961-430f-af2a-2290db51abf0&pf_rd_r=R5DQ8Y1HEGWPJHFZN75Y&pd_rd_wg=bvSWb&pd_rd_r=050d2d1a-56c6-4ad7-9771-fc129c4bd42c&ref_=pd_hp_d_btf_ags-gateway-trending-item&th=1'
    reviews_df = scrape_reviews(url)
    
    