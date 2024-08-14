from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from lsg_converter import LSGConverter

#sentiment_task = pipeline("sentiment-analysis", model=f"cardiffnlp/twitter-roberta-base-sentiment-latest",
                          #tokenizer=f"cardiffnlp/twitter-roberta-base-sentiment-latest")
def start_model():
    
    MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    converter = LSGConverter(max_sequence_length=4096)

    transformedModel, transformedTokenizer = converter.convert_from_pretrained(MODEL_NAME, num_global_tokens=7)
    sentiment_task = pipeline("sentiment-analysis", model=transformedModel,
                            tokenizer=transformedTokenizer)
    return sentiment_task

def analyseSentiment(sentiment_task, text):
    sentiment = sentiment_task(text)
    return {'score': round(sentiment[0]['score'],2), 'label': sentiment[0]['label'].capitalize()}

def analyseMultiple(reviews):
    ooo = start_model()
    for review in reviews:
        print(analyseSentiment(ooo, review))


#listOfreviews = ["I hate this", "A little pricey but worth it", "Easy to assemble", "Design could be improved", "Reliable and durable", "Perfect for everyday use", "Shipping was prompt and packaging was secure", "Customer support was responsive", "A bit heavy but very sturdy", "Great value for money", "Compact and efficient", "Battery life is impressive", "Slightly difficult to use at first", "Functions as expected", "Modern design with sleek finishes", "Instructions were clear and easy to follow", "Could benefit from additional features", "Quiet operation", "Long-lasting and dependable", "The color options are limited", "Performance exceeds expectations", "Worth every penny", "Maintenance is simple", "Not as portable as I hoped", "Highly recommend for professionals", "The build feels cheap", "Satisfactory overall", "Ideal for home use", "The warranty service was quick", "Better than similar products in its price range", "Great for its intended purpose", "The user manual could be more detailed", "Quick and easy setup", "Sturdy construction", "Somewhat noisy but not bothersome", "Customer service was average", "Value for money is excellent", "Attractive design", "A bit bulky for travel", "Works perfectly with other devices", "Feels premium and high-end", "Could use a software update", "Overall very satisfied with the purchase", "The product arrived as described", "Slightly challenging to install", "Performance is consistent and reliable", "Delivery was slower than expected", "Affordable and functional", "Quality control could be improved", "Very stylish and high-quality", "Ideal for office use", "The product does not match the description exactly", "Excellent durability and design", "Could use more customization options", "Good product for its price", "The material feels high-quality", "Works well but has a learning curve", "Would buy again", "The customer support experience was great", "Slightly disappointed with the size", "The product performs well under stress", "Ideal for occasional use", "The price point is just right", "Not as intuitive as expected", "Overall, a solid purchase", "The finish looks beautiful", "Performance is as advertised", "Compact and portable", "The setup process was straightforward", "Good value, but could be better", "The design is a bit outdated", "It performs better than expected", "Shipping packaging could be improved", "A reliable choice for the price", "Great for beginners", "The product looks and feels premium", "The manual lacks depth", "Overall, a good investment", "The product is not very user-friendly", "Excellent craftsmanship and build", "A bit too complex for casual use", "The color options are very basic", "Quality is top-notch", "The product meets all my needs", "A good buy for the features", "Packaging was environmentally friendly", "A little underwhelming, but functional", "Would recommend with some reservations", "The product is exactly what I needed", "Slightly bulky but still effective", "The build quality is impressive", "Not the best for frequent travel", "Works well for the intended purpose", "Delivery was on time", "Product lives up to its reputation", "Good overall performance", "The material feels a bit flimsy", "Customer service could be improved", "Satisfied with the overall experience", "The product exceeded my expectations", "A bit of a hassle to return", "Good value for the investment", "Design is aesthetically pleasing", "Performance has been consistent", "The user experience is smooth", "A solid addition to my collection", "Slightly more complicated than anticipated", "Ideal for specific use cases", "Product is as described", "Happy with the functionality", "The price reflects the quality", "The design is practical and functional", "Shipping was efficient and on time"]
#print(analyseMultiple(listOfreviews))