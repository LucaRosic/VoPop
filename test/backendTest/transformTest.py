import os
import sys
import unittest

# Dynamically add the backend folder to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../backend/Clean'))
sys.path.insert(0, project_root)

from Transform import clean_transform_data 

class TestCleanTransformData(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "Category": "Amazon",
            "Product Name": "100PCS Magnetic Tiles STEM Building Toys Set with 2 Cars, Sensory Stacking Magnetic Blocks for Toddlers & Kids, Ideal for Preschool Montessori Toys Christmas Birthday Gifts for Boys & Girls Ages 3+",
            "Product Image": "https://m.media-amazon.com/images/I/91UUewlD7BL._AC_SX679_.jpg",
            "Unique Key": "B0BVVF6V1S",
            "Clean URL": "https://www.amazon.com.au/Magnetic-Building-Preschool-Montessori-Christmas/dp/B0BVVF6V1S",
            "Average Star": "4.5 out of 5 stars",
            "Brand": "Coodoo",
            "Reviews": [
                {"Review Text": "Great product!", "Date": "2023-09-10", "Stars": "5.0 out of 5"},
                {"Review Text": "Produit incroyable!", "Date": "2023-09-08", "Stars": "5.0 sur 5"},
                {"Review Text": "This is sh*t", "Date": "2023-09-07", "Stars": "4.0 out of 5"},
                {"Review Text": "Not good", "Date": "2023-09-06", "Stars": None},
                {"Review Text": "", "Date": "2023-09-05", "Stars": "3.0 out of 5"},
                {"Review Text": "Average quality", "Date": "2023-09-04", "Stars": "Three stars"}
            ]
        }
    
    def test_language_detection(self):
        print("testing for language_detection--->")
        cleaned_data = clean_transform_data(self.sample_data)
        reviews = cleaned_data['Reviews']
        # Only English reviews should remain
        self.assertEqual(len(reviews), 2)  
        texts = [review['Review Text'] for review in reviews]
        
        self.assertNotIn('Produit incroyable!', texts)
        self.assertNotIn('', texts) #Empty text should not ne in reviews
        
        
        
    
    def test_profanity_filtering(self):
        print("testing for profanity_filtering-->")
        cleaned_data = clean_transform_data(self.sample_data)
        reviews = cleaned_data['Reviews']
        profane_review = next((r for r in reviews if '****' in r['Review Text']), None)
        
        self.assertIsNotNone(profane_review)
        self.assertIn('****', profane_review['Review Text'])


    def test_rating_extraction(self):
        print("testing for rating extraction--->")
        cleaned_data = clean_transform_data(self.sample_data)
        reviews = cleaned_data['Reviews']
        for review in reviews:
            if review['Stars'] is not None:
                self.assertIsInstance(review['Stars'], float)
        avg_star = cleaned_data['Average Stars']
        
        self.assertIsInstance(avg_star, float)
        self.assertEqual(avg_star, 4.5)


    def test_data_cleaning(self):
        print("testing for data cleaning--->")
        cleaned_data = clean_transform_data(self.sample_data)
        self.assertIn('Product Name', cleaned_data)
        
        self.assertEqual(cleaned_data['Product Name'], '100PCS Magnetic Tiles STEM Building Toys Set with 2 Cars, Sensory Stacking Magnetic Blocks for Toddlers & Kids, Ideal for Preschool Montessori Toys Christmas Birthday Gifts for Boys & Girls Ages 3+')
        self.assertIn('Brand', cleaned_data)
        self.assertEqual(cleaned_data['Brand'], 'Coodoo')


    def test_missing_data_handling(self):
        print("testing for missing data handlings--->")
        cleaned_data = clean_transform_data(self.sample_data)
        reviews = cleaned_data['Reviews']
        texts = [review['Review Text'] for review in reviews]
        
        self.assertNotIn('', texts)  # Review with empty text should be removed
        # Check if 'Stars' is None for the appropriate review
        for review in reviews:
            if review['Review Text'] == 'Not good':
                
                self.assertIsNone(review['Stars'])


    def test_various_rating_formats(self):
        print("testing for various rating format--->")
        cleaned_data = clean_transform_data(self.sample_data)
        reviews = cleaned_data['Reviews']
        for review in reviews:
            if review['Review Text'] == 'Average quality':
                
                self.assertEqual(review['Stars'], 3.0)
                
if __name__ == '__main__':
    unittest.main()