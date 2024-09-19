import os
import sys
import unittest

# Dynamically add the backend folder to sys.path to import sentiment.py
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../backend/ML'))
sys.path.insert(0, project_root)

# Import the necessary functions from sentiment.py
from sentiment import start_model, analyseSentiment

class TestSentimentAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Class-level setup that runs once before all tests.
        Initializes the sentiment analysis model and reuses it for all test cases.
        """
        cls.sentiment_task = start_model()
        
    
    def test_positive_sentiment(self):
        text = "I love this product!"
        expected_label = "Positive"
        result = analyseSentiment(self.sentiment_task, text)
        self.assertEqual(result['label'], expected_label)
        
    
    def test_negative_sentiment(self):
        text = "The product didn't work at all."
        expected_label = "Negative"
        result = analyseSentiment(self.sentiment_task, text)
        self.assertEqual(result['label'], expected_label)
        
    
    def test_neutral_sentiment(self):
        text = "The product is just okay, nothing special."
        expected_label = "Neutral"
        result = analyseSentiment(self.sentiment_task, text)
        self.assertEqual(result['label'], expected_label)
        
        
    def test_positive_emoji(self):
        text = "I am so happy with the product 😊"
        expected_label = "Positive"
        result = analyseSentiment(self.sentiment_task, text)
        self.assertEqual(result['label'], expected_label)
        
    
    def test_negative_emoji(self):
        text = "This is bad 😢"
        expected_label = "Negative"
        result = analyseSentiment(self.sentiment_task, text)
        self.assertEqual(result['label'], expected_label)
        
    
    def test_only_emoji_positive(self):
        text = "😍"
        expected_label = "Positive"
        result = analyseSentiment(self.sentiment_task, text)
        self.assertEqual(result['label'], expected_label)
        
    
    def test_only_emoji_negative(self):
        text = "😠"
        expected_label = "Negative"
        result = analyseSentiment(self.sentiment_task, text)
        self.assertEqual(result['label'], expected_label)
        
        
    def test_confusing_text(self):
        text = "Not bad at all."
        expected_label = "Positive"  # Even though it contains 'not bad', it's positive
        result = analyseSentiment(self.sentiment_task, text)
        self.assertEqual(result['label'], expected_label)
        
    
    def test_empty_string(self):
        text = ""
        expected_label = "Neutral" 
        result = analyseSentiment(self.sentiment_task, text)
        self.assertEqual(result['label'], expected_label)
        
    
    def test_special_characters(self):
        text = "@#$%^&*()!"
        expected_label = "Negative"
        result = analyseSentiment(self.sentiment_task, text)
        self.assertEqual(result['label'], expected_label)
        
    
    
if __name__ == '__main__':
    unittest.main()