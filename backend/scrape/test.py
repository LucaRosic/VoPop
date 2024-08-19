from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random 

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
                review_elements = pop_out_window.find_elements(By.CLASS_NAME, "list--wrap--KBzXADx")
                
                if not review_elements:
                    print("No more reviews found.")
                    break
                
                for review in review_elements:
                    reviews_list.append(review.text)
                    print(f"Review {review_index}: {review.text}")
                    review_index += 1
                
                # Add a delay to avoid being blocked
                time.sleep(random.randint(1, 5))
                
            except Exception as e:
                print(f"Error while extracting reviews: {e}")
                break

    except Exception as e:
        print(f"Error: {e}")
    
    # Keep the browser open
    input("Press Enter to close the browser...")
    driver.quit()


    scrape_ali_express_reviews('https://www.aliexpress.com/item/1005001629825915.html')