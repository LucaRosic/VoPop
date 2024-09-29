import os
import sys
import unittest
import time

# Dynamically add the backend folder to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../scrape'))
print(project_root)
sys.path.insert(0, project_root)

# Importing from the dynamically adjusted path
from scrapper import scrape_reviews, clean_url  

class TestScraperFunctions(unittest.TestCase):
    
    def setUp(self):
        # Setup URLs to be used in tests
        self.amazon_url = 'https://www.amazon.com.au/Magnetic-Building-Preschool-Montessori-Christmas/dp/B0BVVF6V1S?pd_rd_w=r3VyS&content-id=amzn1.sym.36bbdb86-b7cf-4ece-b220-7744a3b6a603&pf_rd_p=36bbdb86-b7cf-4ece-b220-7744a3b6a603&pf_rd_r=R5DQ8Y1HEGWPJHFZN75Y&pd_rd_wg=bvSWb&pd_rd_r=050d2d1a-56c6-4ad7-9771-fc129c4bd42c&pd_rd_i=B0BVVF6V1S&ref_=pd_hp_d_btf_unk_B0BVVF6V1S'
        self.amazon_cleanurl = "https://www.amazon.com.au/Magnetic-Building-Preschool-Montessori-Christmas/dp/B0BVVF6V1S"
        self.amazon_review_url = "https://www.amazon.com/product-reviews/B08J5F3G18/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        self.expected_amazon_clean_url = "https://www.amazon.com/dp/B08J5F3G18"
        
        self.aliexpress_url = "https://www.aliexpress.com/item/1005007003675009.html?spm=a2g0o.tm1000008910.d0.1.1fd970c8Z8cI5p&pvid=74441cc0-f36e-477d-ba29-a50ec039cc9a&pdp_ext_f=%7B%22ship_from%22:%22CN%22,%22list_id%22:286001,%22sku_id%22:%2212000039016093172%22%7D&scm=1007.25281.317569.0&scm-url=1007.25281.317569.0&scm_id=1007.25281.317569.0&pdp_npi=4%40dis%21AUD%21AU%20%2410.23%21AU%20%241.50%21%21%2148.14%217.06%21%402101ec1f17241139124465114edd7d%2112000039016093172%21gdf%21AU%21%21X&aecmd=true"
        self.expected_aliexpress_clean_url = "https://www.aliexpress.com/item/1005007003675009.html"
    
    def test_scrape_reviews_time(self):
        """Test that scrape_reviews function executes within the time limit for Amazon."""
        start_time = time.time()
        
        try:
            scrape_reviews(self.amazon_url)
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"Execution time: {execution_time:.2f} seconds")
            self.assertLess(execution_time, 60, "Scraper took longer than 60 seconds")
        
        except Exception as e:
            self.fail(f"Scraping failed due to an unexpected error: {e}")


    def test_clean_amazon_url(self):
        """Test cleaning an Amazon URL with review query parameters."""
        try:
            cleaned_url, _ = clean_url(self.amazon_review_url)
            
            print(f"Expected Cleaned URL: {self.expected_amazon_clean_url}, Actual Cleaned URL: {cleaned_url}")
            self.assertEqual(cleaned_url, self.expected_amazon_clean_url, f"Cleaned URL: {cleaned_url}")
        
        except Exception as e:
            self.fail(f"Clean Amazon URL test failed due to an unexpected error: {e}")

    #def test_scrape_aliexpress_reviews_time(self):
        # """Test that scrape_reviews function executes within the time limit for AliExpress."""
        #start_time = time.time()
        
        #try:
            #scrape_reviews(self.aliexpress_url)
            #end_time = time.time()
        #     execution_time = end_time - start_time
            
        #     print(f"Execution time: {execution_time:.2f} seconds")
        #     self.assertLess(execution_time, 60, "AliExpress scraper took longer than 60 seconds")
        
        # except Exception as e:
        #     self.fail(f"AliExpress scraping failed due to an unexpected error: {e}")

    def test_clean_aliexpress_url(self):
        """Test cleaning an AliExpress URL with additional query parameters."""
        try:
            cleaned_url, _ = clean_url(self.aliexpress_url)
            
            print(f"Expected Cleaned URL: {self.expected_aliexpress_clean_url}, Actual Cleaned URL: {cleaned_url}")

            self.assertEqual(cleaned_url, self.expected_aliexpress_clean_url, f"Cleaned URL: {cleaned_url}")
        
        except Exception as e:
            self.fail(f"Clean AliExpress URL test failed due to an unexpected error: {e}")

if __name__ == "__main__":
    unittest.main()