from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    elif 'aliexpress' in url:
        return 'aliexpress'
    else:
        return None
    
def clean_url(url):
    if get_site(url) == 'amazon':
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
    gecko_driver_path = r''

    # Configure Firefox options
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')

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
        print("Product name")
        product_image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'landingImage'))
        ).get_attribute('src')
        print("Image")

        avg_star = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#cm_cr_dp_d_rating_histogram > div.a-fixed-left-grid.AverageCustomerReviews.a-spacing-small > div > div.a-fixed-left-grid-col.aok-align-center.a-col-right > div > span > span'))
        ).text
        print("Star")

        

        # Click on the "See more reviews" link if present
        try:
            see_more_reviews = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-hook="see-all-reviews-link-foot"]'))
            )
            see_more_reviews.click()
        except Exception as e:
            print("See more reviews link not found or error:", e)

        try:
            most_recent_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'a-autoid-3-announce'))
            )
            most_recent_button.click()
        except Exception as e:
            print("review type not found reviews link not found or error:", e)
        try:
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

        while True:
            # Extract review elements
            review_elements = WebDriverWait(driver, 15).until(
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

    # Create a product details dictionary
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

    # Save product details as a JSON file
    with open('amazon_product_details.json', 'w') as file:
        json.dump(product_details, file, indent=4)

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Scraping completed in {elapsed_time:.2f} seconds")

    return product_details

def scrape_ali_express_reviews(url):
    print("AliExpress detected")
    start_time = time.time()
    
    # Specify the path to your GeckoDriver executable
    gecko_driver_path = r''  # Add your path here

    # Configure Firefox options
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')

    # Initialize FirefoxDriver service
    service = Service(gecko_driver_path)

    # Initialize Firefox WebDriver with service and options
    driver = webdriver.Firefox(service=service, options=options)

    # Initialize an empty list to store reviews
    reviews_list = []
    
    try:
        # Open the product page
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # Click the reviews section to open the pop-up window
        reviews_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#nav-review > div:nth-child(2) > button > span"))
        )
        reviews_button.click()
        time.sleep(5)  # Wait for the pop-out window to appear

        # Wait for the pop-out window to appear and store it in the variable
        pop_out_window = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[12]/div[2]/div/div[2]/div/div/div/div[4]/div/div[2]/div/div[3]"))
        )
        print("Pop-out window found.")

        # Loop to extract reviews
        review_index = 1
        while True:
            try:
                # Find all review elements within the pop-out window
                review_elements = pop_out_window.find_elements(By.CLASS_NAME, "list--itemReview--hBFPNly")
                
                if not review_elements:
                    print("No more reviews found.")
                    break

                # Extract reviews
                for review_element in review_elements:
                    # Extract review text
                    review_text = review_element.text
                    
                    # Extract review date (if available)
                    review_date = "Date not found"  # Set a default value
                    try:
                        review_date_element = review_element.find_element(By.XPATH, ".//following-sibling::div[contains(@class, 'list--itemInfo--fb1A_M1')]")
                        review_date = review_date_element.text
                    except Exception as e:
                        print("Error finding review date:", e)
                    
                    # Extract star rating (if available)
                    star_elements = review_element.find_elements(By.XPATH, ".//following-sibling::div[contains(@class, 'stars--box--vHzUWQ9')]//span[contains(@class, 'comet-icon-starreviewfilled')]")
                    review_stars = len(star_elements)
                    
                    # Append the extracted data to the reviews list
                    reviews_list.append({
                        'Date': review_date,
                        'Stars': review_stars,
                        'Review Text': review_text
                    })
                    
                # Scroll after every 20 reviews
                if review_index % 20 == 0:
                    driver.execute_script("arguments[0].scrollIntoView();", review_elements[-1])

                    # Asynchronous wait to ensure new reviews are loaded
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "list--itemReview--hBFPNly"))
                    )
                    
                review_index += len(review_elements)
                
            except Exception as e:
                print("Error extracting review details:", e)
                break

    except Exception as e:
        print("Error loading reviews:", e)

    finally:
        # Close the WebDriver
        driver.quit()

    # Save product details as a JSON file
    with open('aliexpress_product_details.json', 'w') as file:
        json.dump(reviews_list, file, indent=4)

    print(f"Scraped {len(reviews_list)} reviews from AliExpress")
    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Scraping completed in {elapsed_time:.2f} seconds")

    return reviews_list



def scrape_reviews(url):
    if not is_valid_url(url):
        print("Invalid URL")
        return None

    site = get_site(url)
    if site == 'amazon':
        return scrape_amazon_reviews(url)
    elif site == 'etsy':
        return scrape_ali_express_reviews(url)
    elif site == 'aliexpress':
        return scrape_ali_express_reviews(url)
    else:
        print("Unsupported site")
        return None


if __name__ == "__main__":
    # url = "https://www.etsy.com/au/listing/1518307138/personalized-travel-jewelry-box-small?click_key=e840c0f4cb9842b5b33c7993184a9c63c837c426%3A1518307138&click_sum=dd8b8e24&ref=hp_prn-1&pro=1&sts=1"
    # url = "https://www.aliexpress.com/item/1005006598161696.html?spm=a2g0o.detail.pcDetailBottomMoreOtherSeller.1.170acr2ncr2nwm&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.40000.326746.0&scm_id=1007.40000.326746.0&scm-url=1007.40000.326746.0&pvid=5206a737-b0cc-4b82-9da6-d6300fc3301d&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.40000.326746.0,pvid:5206a737-b0cc-4b82-9da6-d6300fc3301d,tpp_buckets:668%232846%238114%23750&pdp_npi=4%40dis%21AUD%2110.32%211.52%21%21%2148.05%217.06%21%402101e62517237011224783085eb4b6%2112000037771136223%21rec%21AU%21%21ABX&utparam-url=scene%3ApcDetailBottomMoreOtherSeller%7Cquery_from%3A"
    
    url = 'https://www.amazon.com.au/Magnetic-Building-Preschool-Montessori-Christmas/dp/B0BVVF6V1S?pd_rd_w=r3VyS&content-id=amzn1.sym.36bbdb86-b7cf-4ece-b220-7744a3b6a603&pf_rd_p=36bbdb86-b7cf-4ece-b220-7744a3b6a603&pf_rd_r=R5DQ8Y1HEGWPJHFZN75Y&pd_rd_wg=bvSWb&pd_rd_r=050d2d1a-56c6-4ad7-9771-fc129c4bd42c&pd_rd_i=B0BVVF6V1S&ref_=pd_hp_d_btf_unk_B0BVVF6V1S'
    reviews_df = scrape_reviews(url)