import unittest
import time
from backend.scrape.scrapper import scrape_reviews

class TestScraperExecutionTime(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.amazon.com.au/Magnetic-Building-Preschool-Montessori-Christmas/dp/B0BVVF6V1S?pd_rd_w=r3VyS&content-id=amzn1.sym.36bbdb86-b7cf-4ece-b220-7744a3b6a603&pf_rd_p=36bbdb86-b7cf-4ece-b220-7744a3b6a603&pf_rd_r=R5DQ8Y1HEGWPJHFZN75Y&pd_rd_wg=bvSWb&pd_rd_r=050d2d1a-56c6-4ad7-9771-fc129c4bd42c&pd_rd_i=B0BVVF6V1S&ref_=pd_hp_d_btf_unk_B0BVVF6V1S'
        self.cleanurl = "https://www.amazon.com.au/Magnetic-Building-Preschool-Montessori-Christmas/dp/B0BVVF6V1S"

    def test_scrape_reviews_time(self):
        start_time = time.time()
        
        try:
            scrape_reviews(self.url)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"Execution time: {execution_time:.2f} seconds")

            self.assertLess(execution_time, 35, "Scraper took too longer then 35 seconds")
        
        except Exception as e:
            self.fail(f"Scraping failed due to an unexpected error: {e}")

if __name__ == "__main__":
    unittest.main()

