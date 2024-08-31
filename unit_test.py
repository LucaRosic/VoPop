import unittest
import time
import selenium
from backend.scrape.scrapper import scrape_reviews, clean_url

class TestScraperExecutionTime(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.amazon.com.au/Magnetic-Building-Preschool-Montessori-Christmas/dp/B0BVVF6V1S?pd_rd_w=r3VyS&content-id=amzn1.sym.36bbdb86-b7cf-4ece-b220-7744a3b6a603&pf_rd_p=36bbdb86-b7cf-4ece-b220-7744a3b6a603&pf_rd_r=R5DQ8Y1HEGWPJHFZN75Y&pd_rd_wg=bvSWb&pd_rd_r=050d2d1a-56c6-4ad7-9771-fc129c4bd42c&pd_rd_i=B0BVVF6V1S&ref_=pd_hp_d_btf_unk_B0BVVF6V1S'
        self.cleanurl = "https://www.amazon.com.au/Magnetic-Building-Preschool-Montessori-Christmas/dp/B0BVVF6V1S"

    def test_scrape_reviews_time(self):
        start_time = time.time()
        
        try:
            scrape_reviews(self.url) # Directly use URL from the setUp
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"Execution time: {execution_time:.2f} seconds")

            self.assertLess(execution_time, 35, "Scraper took too longer then 35 seconds")
        
        except Exception as e:
            self.fail(f"Scraping failed due to an unexpected error: {e}")

class TestCleanURL(unittest.TestCase):

    def test_clean_amazon_url(self):
        """Test cleaning an Amazon URL with review query parameters."""
        try:
            url = "https://www.amazon.com/product-reviews/B00X4WHP5E/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
            expected_clean_url = "https://www.amazon.com/dp/B00X4WHP5E"
            cleaned_url, _ = clean_url(url)
            self.assertEqual(cleaned_url, expected_clean_url,f"Cleaned URL: {cleaned_url}")
        
        except Exception as e:
            self.fail(f"Clean Amazon URL test failed due to an unexpected error: {e}")
        

        

if __name__ == "__main__":
    unittest.main()

