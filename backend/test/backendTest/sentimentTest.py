import os
import sys
import unittest

# Dynamically add the backend folder to sys.path to import sentiment.py
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../ML'))
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
        print("testing for positive sentiment label")
        text = "I love this product!"
        expected_label = "Positive"
        result = analyseSentiment(self.sentiment_task, text)
        
        print("output --> ", result , "expected label --> ", expected_label)
        
        self.assertEqual(result['label'], expected_label)
        
    
    def test_negative_sentiment(self):
        print("Testing for negative sentiment label")
        text = "The product didn't work at all."
        expected_label = "Negative"
        result = analyseSentiment(self.sentiment_task, text)
        
        print("output --> ", result , "expected label --> ", expected_label)
        
        self.assertEqual(result['label'], expected_label)
        
    
    def test_neutral_sentiment(self):
        print("testing for neutral sentiment label")
        text = "The product is just okay, nothing special."
        expected_label = "Neutral"
        result = analyseSentiment(self.sentiment_task, text)
        
        print("output --> ", result , "expected label --> ", expected_label)
        
        self.assertEqual(result['label'], expected_label)
        
        
    def test_positive_emoji(self):
        print("testing for positive emoji label")
        text = "I am so happy with the product 😊"
        expected_label = "Positive"
        result = analyseSentiment(self.sentiment_task, text)
        
        print("output --> ", result , "expected label --> ", expected_label)
        
        self.assertEqual(result['label'], expected_label)
        
    
    def test_negative_emoji(self):
        print("testing for negative emoji label")
        text = "This is bad 😢"
        expected_label = "Negative"
        result = analyseSentiment(self.sentiment_task, text)
        
        print("output --> ", result , "expected label --> ", expected_label)
        
        self.assertEqual(result['label'], expected_label)
        
    
    def test_only_emoji_positive(self):
        print("testing for only positive emoji")
        text = "😍"
        expected_label = "Positive"
        result = analyseSentiment(self.sentiment_task, text)
        
        print("output --> ", result , "expected label --> ", expected_label)
        
        self.assertEqual(result['label'], expected_label)
        
    
    def test_only_emoji_negative(self):
        print("testing for only negative emoji")
        text = "😠"
        expected_label = "Negative"
        result = analyseSentiment(self.sentiment_task, text)
        
        print("output --> ", result , "expected label --> ", expected_label)
        
        self.assertEqual(result['label'], expected_label)
        
        
    def test_confusing_text(self):
        print("testing for confusing text label")
        text = "Not bad at all."
        expected_label = "Positive"  # Even though it contains 'not bad', it's positive
        result = analyseSentiment(self.sentiment_task, text)
        
        print("output --> ", result , "expected label --> ", expected_label)
        
        self.assertEqual(result['label'], expected_label)
        
    
    def test_empty_string(self):
        print("testing for empty reviews")
        text = ""
        expected_label = "Neutral" 
        result = analyseSentiment(self.sentiment_task, text)
        
        print("output --> ", result , "expected label --> ", expected_label)
        
        self.assertEqual(result['label'], expected_label)
        
    
    def test_special_characters(self):
        print("testing for special characters")
        text = "@#$%^&*()!"
        expected_label = "Negative"
        result = analyseSentiment(self.sentiment_task, text)
        
        print("output --> ", result , "expected label --> ", expected_label)
        
        self.assertEqual(result['label'], expected_label)
        
    
    
if __name__ == '__main__':
    unittest.main()