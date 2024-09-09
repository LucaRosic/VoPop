from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re
import time
from urllib.parse import urlparse
from selenium import webdriver

# from airflow.decorators import dag, task

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_site(url):
    if 'amazon' in url:
        return 'amazon'
    elif 'aliexpress' in url:
        return 'aliexpress'
    else:
        return None
    
def clean_url(url):
    if "amazon.com" in url:
        if "/product-reviews/" in url:
            url = url.replace("/product-reviews/", "/dp/")
            
        if "/dp/" in url:
            parts = url.split("/dp/")
            clean_part = parts[1].split("/ref")[0] if "/ref" in parts[1] else parts[1].split("?")[0]
            return parts[0] + "/dp/" + clean_part, clean_part

    elif "aliexpress.com" in url:
        if "/item/" in url:
            parts = url.split("/item/")
            if ".html" in parts[1]:
                clean_part = parts[1].split(".html")[0]
            else:
                clean_part = parts[1].split("?")[0]
            return parts[0] + "/item/" + clean_part + ".html", clean_part

    return url


def convert_date(date_str):
    if date_str is None:
        raise ValueError("Date is None")
    
    # Check if the date string contains a '|' and extract the part after it
    if '|' in date_str:
        cleaned_date_str = date_str.split('|')[1].strip()
    else:
        # Remove any leading text before the actual date using "on" as a reference point
        cleaned_date_str = re.sub(r'^.*on\s+', '', date_str).strip()
    
    # Try to parse the cleaned date string with different formats
    for fmt in ('%Y-%m-%d','%d %B %Y', '%B %d %Y', '%B %d, %Y','%d %b %Y'):
        try:
            date_obj = datetime.strptime(cleaned_date_str, fmt)
            return date_obj#.strftime('%d %B %Y')  # Return the datetime object
        except ValueError:
            pass
    
    raise ValueError(f'No valid date format found for {date_str}')




def scrape_amazon_reviews(url,date_filter=None):
    count=0 
    print("Amazon detected")
    start_time = time.time()

    # Specify the path to your GeckoDriver executable
    gecko_driver_path = r''

    # Configure Firefox options
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    #options.add_argument('--headless') 

    # Initialize FirefoxDriver service
    service = Service(gecko_driver_path)

    # Initialize Firefox WebDriver with service and options
    driver = webdriver.Firefox(service=service, options=options)

    # Clean the URL
    cleaned_url, unique_key = clean_url(url)
    driver.get(cleaned_url)

    # Initialize an empty list to store reviews
    reviews_list = []

    if date_filter is None:
        try:
            print('Looking for product name')
            product_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'productTitle'))
            ).text
            print(f'Product name found: {product_name}')

            print('Looking for product image')
            product_image = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'landingImage'))
            ).get_attribute('src')
            print(f'Product image found: {product_image}')

            print('Looking for avg star')
            avg_star = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#cm_cr_dp_d_rating_histogram > div.a-fixed-left-grid.AverageCustomerReviews.a-spacing-small > div > div.a-fixed-left-grid-col.aok-align-center.a-col-right > div > span > span'))
            ).text
            print(f'Average star rating found: {avg_star}')

            print('Looking for product brand')
            try:
                # First attempt with the primary selector
                product_brand = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#cr-arp-byline > a'))
                ).text
                print(f'Product brand found using primary selector: {product_brand}')
            except Exception as e:
                print(f'Primary selector failed, trying alternative. Error: {e}')
                try:
                    # Secondary attempt with the alternative selector
                    product_brand = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'bylineInfo'))
                    ).text
                    print(f'Product brand found using secondary selector: {product_brand}')
                except Exception as e:
                    print(f'Secondary selector also failed. Error: {e}')
                    product_brand = "NA"

        except Exception as e:
            print("Error extracting product details:", e)
            product_name = "NA"
            product_image = "NA"
            avg_star = "NA"
            
    else:
        print("Skipping product information due to date filter.")

    try:
        try:
            print("searching.....more reviews")
            see_more_reviews = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-hook="see-all-reviews-link-foot"]'))
            )
            see_more_reviews.click()
        except Exception as e:
            print("See more reviews link not found or error:", e)
        try:
            product_brand = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'a-size-base a-link-normal'))
            ).text
            print(f'Product brand found using third selector: {product_brand}')
        except Exception as e:
            print(f'Secondary selector also failed. Error: {e}')
            product_brand = "NA"

        try:
            print("searching.....butonnnnnnnnnnnnnn")
            see_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span.a-button-text.a-declarative")))
            print("button found")
            see_more_button.click()     
        except Exception as e:
            print("review type not found reviews link not found or error:", e)
        try:
            print('most recent attempt')
            most_recent = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'sort-order-dropdown_1'))
            )
            most_recent.click()
        except Exception as e:
            print("most recent reviews link not found or error:", e)
        try:
            product_brand = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#cr-arp-byline > a'))
            ).text
        except:
            product_brand = "NA"
        time.sleep(1)
        while True:
            # Extract review elements
            review_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.a-section.review'))
            )

            # Iterate over each review element
            for review in review_elements:
                
                try:
                    # Extract review text
                    review_text = review.find_element(By.CSS_SELECTOR, '.review-text-content').text
                    # Extract review date
                    review_date = review.find_element(By.CSS_SELECTOR, '.review-date').text

                    try:
                        review_date = convert_date(review_date)
                    except ValueError as e:
                        print(f"Error cleaning date: {e}")
                        review_date = None
                    # Convert the date filter to a datetime object
                    review_date_str = review.find_element(By.CSS_SELECTOR, '.review-date').text
                    review_date = convert_date(review_date_str)  # Convert to datetime object

                    # Skip reviews based on the date filter
                    if date_filter and review_date <= convert_date(date_filter):
                        print(f"Skipping review from {review_date} due to date filter: {date_filter}")
                        continue

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

    if date_filter:
        return reviews_list

    # If no date_filter, return product details along with reviews
    product_details = {
        'Category': 'Amazon',
        'Product Name': product_name,
        'Product Image': product_image,
        'Unique Key': unique_key,
        'Clean URL': cleaned_url,
        'Brand': product_brand,
        'Average Star': avg_star,
        'Reviews': reviews_list
    } 

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Scraping completed in {elapsed_time:.2f} seconds")

    return product_details


def scrape_ali_express_reviews(url):
    
    print("AliExpress detected")

    # Specify the path to your GeckoDriver executable
    gecko_driver_path = r''  # Add your path here

    # Configure Firefox options
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    # Initialize FirefoxDriver service
    service = Service(gecko_driver_path)

    # Initialize Firefox WebDriver with service and options
    driver = webdriver.Firefox(service=service, options=options)

    cleaned_url, unique_key = clean_url(url)
    

    # Initialize an empty list to store reviews
    reviews_list = []
    review_index = 1
    reviews_per_page = 20  # Number of reviews loaded per page

    try:
        # Open the product page
        driver.get(cleaned_url)
        time.sleep(2)  # Wait for the page to load
        
        product_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'title--wrap--UUHae_g'))
        ).text
        print("Product name")
        time.sleep(1)

        product_image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/div[1]/div[1]/div/div/div[2]/div[1]/div/img'))
        ).get_attribute('src')
        print("Image")
        time.sleep(1)

        avg_star = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#nav-review > div:nth-child(2) > div.header--wrap--BgjROgu > div > div.header--blockWrap1--S_r1OlE > div > div.header--num--XJ6wKJ5'))
        ).text
        print("Star")
        time.sleep(1)

        product_brand = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#nav-specification > ul > li:nth-child(3) > div:nth-child(2) > div.specification--desc--Dxx6W0W'))
        ).text
        print("Product brand")
        time.sleep(1)
        # Click the reviews section to open the pop-up window
        reviews_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#nav-review > div:nth-child(2) > button > span"))
        )
        reviews_button.click()
        time.sleep(5)  # Wait for the pop-out window to appear

        # Wait for the pop-out window to appear and store it in the variable
        try:
            pop_out_window = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "comet-v2-modal-body"))
            )
            print("Pop-out window found.")
        except Exception as e:
            print("Error finding pop-out window:", e)
            driver.quit()
            return

        # Function to construct the XPath for review elements
        def get_review_xpath(index):
            # Test both potential structures
            xpath_1 = f"/html/body/div[12]/div[2]/div/div[2]/div/div/div/div[4]/div/div[{index}]/div/div[3]/div[1]/div[3]"
            xpath_2 = f"/html/body/div[12]/div[2]/div/div[2]/div/div/div/div[4]/div/div[{index}]/div/div[2]/div[1]/div[3]"
            try:
                element = pop_out_window.find_element(By.XPATH, xpath_1)
                return xpath_1
            except Exception as e:
                try:
                    element = pop_out_window.find_element(By.XPATH, xpath_2)
                    return xpath_2
                except Exception as e:
                    raise Exception(f"Unable to locate review element at index {index}")
        empty_count = 0
        # Loop to extract reviews
        while True:
            try:
                # Construct the XPath for the review container based on the index
                review_xpath = get_review_xpath(review_index)
                # Try to find the review element
                review_element = pop_out_window.find_element(By.XPATH, review_xpath)
                
                # Extract review text
                review_text = review_element.text
                print(review_text)
                        # Check if the review text is empty
                if not review_text:
                    empty_count += 1
                    print(f"Empty review found. Count: {empty_count}")
                else:
                    empty_count = 0  # Reset counter if a non-empty review is found

                # Stop scraping if 5 consecutive empty reviews are found
                if empty_count >= 5:
                    print("5 consecutive empty reviews found. Stopping scraping.")
                    break

                # Extract review date
                try:
                    review_date_xpath = review_xpath.replace("div[1]/div[3]", "div[2]/div[1]")
                    review_date = pop_out_window.find_element(By.XPATH, review_date_xpath).text
                except Exception as e:
                    review_date = "Date not found"
                    print("Error finding review date:", e)
                
                try:
                    # Find the star box using the class name relative to the review element
                    star_box = review_element.find_element(By.CLASS_NAME, "comet-icon-starreviewfilled")
                    
                    # Find all filled stars within the star box
                    filled_stars = review_element.find_elements(By.CLASS_NAME, "comet-icon-starreviewfilled")
                    
                    # Count the number of filled stars
                    review_stars = len(filled_stars)
                    
                    print(f"{review_stars} total stars for the review.")
                except Exception as e:
                    print(f"An error occurred while finding stars: {e}")
                    review_stars = 0

                        
                # Append the extracted data to the reviews list
                reviews_list.append({
                    'Date': review_date,
                    'Stars': review_stars,
                    'Review Text': review_text
                })
                
                # Increment the review index
                review_index += 1
                
                # Scroll down every reviews_per_page reviews to load more
                if (review_index - 1) % reviews_per_page == 0:
                    print("Scrolling down to load more reviews...")
                    driver.execute_script("arguments[0].scrollIntoView(true);", review_element)
                    time.sleep(2) 

            except Exception as e:
                # Exit the loop if no more reviews are found or if an error occurs
                if "no such element" in str(e).lower():
                    print("No more reviews found or error encountered.")
                    break
                print("Error extracting review details:", e)
                break

    except Exception as e:
        print("Error loading reviews:", e)

    finally:
        # Close the WebDriver
        driver.quit()
    # Create a product details dictionary
    product_details = {
        'Category': 'AliExpress',
        'Product Name': product_name,
        'Product Image': product_image,
        'Unique Key': unique_key,
        'Clean URL': cleaned_url,
        'Brand': product_brand,
        'Average Star': avg_star,
        'Reviews': reviews_list
    }
    # Save product details as a JSON file
    with open('aliexpress_product_details.json', 'w') as file:
        json.dump(product_details, file, indent=4)

    print(f"Scraped {len(reviews_list)} reviews from AliExpress")

    return reviews_list

def scrape_reviews(url, *date):
    if not is_valid_url(url):
        print("Invalid URL")
        return None

    site = get_site(url)

    if site == 'amazon':
        return scrape_amazon_reviews(url, date)
    elif site == 'etsy':
        return scrape_ali_express_reviews(url)
    elif site == 'aliexpress':
        return scrape_ali_express_reviews(url)
    else:
        print("Unsupported site")
        return None


if __name__ == "__main__":

    # url = "https://www.aliexpress.com/item/1005007003675009.html?spm=a2g0o.tm1000008910.d0.1.1fd970c8Z8cI5p&pvid=74441cc0-f36e-477d-ba29-a50ec039cc9a&pdp_ext_f=%7B%22ship_from%22:%22CN%22,%22list_id%22:286001,%22sku_id%22:%2212000039016093172%22%7D&scm=1007.25281.317569.0&scm-url=1007.25281.317569.0&scm_id=1007.25281.317569.0&pdp_npi=4%40dis%21AUD%21AU%20%2410.23%21AU%20%241.50%21%21%2148.14%217.06%21%402101ec1f17241139124465114edd7d%2112000039016093172%21gdf%21AU%21%21X&aecmd=true"
    
    # url = 'https://www.amazon.com.au/Magnetic-Building-Preschool-Montessori-Christmas/product-reviews/B0BVVF6V1S/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
        url='https://www.amazon.com/Apple-Smartwatch-Starlight-Aluminum-Detection/product-reviews/B0CHX7R6WJ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
        date = datetime(day=2,month=7, year=2024)
        reviews_df = scrape_reviews(url)
