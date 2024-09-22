import re
from langdetect import detect
from better_profanity import profanity

# Initialize the better-profanity library
profanity.load_censor_words()

def clean_rate(rate):
    """
    Cleans and extracts the numerical rating from a string or retains it if already a float.
    Args:
        rate (str or float): The rating value, which can be a string (e.g., '4.5 out of 5 stars') 
                        or a float.
    Returns:
        float or None: The cleaned rating as a float, or `None` if it cannot be extracted.
    """

    if isinstance(rate, str):
        try:
            # Amazon 
            match = re.findall(r'\d+\.\d+|\d+', rate)  
            if match:
                rate = float(match[0])  
            else:
                rate = None
        except (ValueError, IndexError):
            rate = None        
    elif isinstance(rate, (float, int)):
        # AliExpress
        rate = float(rate)
    else:
        rate = None
    return rate

def clean_transform_data(data):
    """
    Cleans and transforms the product review data.

    The function extracts product information (e.g., category, name, brand) and reviews from
    the input data, then processes each review by:
    - Filtering out non-English reviews
    - Censoring profanity
    - Standardising star ratings
    
    The cleaned data is returned with both product info and the cleaned reviews

    Args:
        data (dict): The raw product data that includes category, product name, brand, reviews, etc.

    Returns:
        dict: A dictionary containing cleaned product information and cleaned reviews
            Product Information:
                - 'Category' (str): The category of the product
                - 'Product Name' (str): The name of the product
                - 'Product Image' (str): The image URL of the product
                - 'Unique Key' (str): A unique identifier for the product
                - 'Clean URL' (str): A cleaned and standardized URL for the product
                - 'Brand' (str): The brand of the product
                - 'Average Stars' (float): The average star rating for the product

    Cleaned Reviews (list of dicts):
        - 'Date' (str): The date of the review
        - 'Stars' (float or None): The cleaned and standardized star rating
        - 'Review Text' (str): The review text with profanity censored
    """
   
    cleaned_reviews = []
    
    # Extract product information
    category = data.get("Category","")
    product_name = data.get("Product Name", "")   
    product_image = data.get("Product Image", "")
    unique_key = data.get("Unique Key", "")
    clean_url = data.get("Clean URL","")
    avg_star = data.get("Average Star","")
    brand = data.get("Brand", "")

    if "Brand: " in brand:
        brand=brand.split(":",1)[1].strip()
    
    # Extract the reviews
    reviews = data.get("Reviews", [])

    for review in reviews:
        review_text = review.get('Review Text', '')
        review_date = review.get('Date', '')
        review_rating = review.get('Stars', '')

        try:# Remove Non-English reviews
            if detect(review_text) != 'en':
                ####print('not good')
                continue
        except:
            ####print("this shit borken")
            continue

        # Filter out profanity
        review_text = profanity.censor(review_text)

        
        if review_rating:
            review_rating = clean_rate(review_rating)
        if category == 'Amazon':
            avg_star = clean_rate(avg_star)


        cleaned_review = {
            'Date': review_date,
            'Stars': review_rating,
            'Review Text': review_text
        }
        cleaned_reviews.append(cleaned_review)
    
    # Return the complete data including product info and cleaned reviews
    return {
        'Category': category,
        'Product Name': product_name,
        'Product Image': product_image,
        'Unique Key': unique_key,
        'Clean URL': clean_url,
        'Brand': brand,
        'Average Stars': avg_star,
        'Reviews': cleaned_reviews
    }


if __name__ == "__main__":
    file = {
    "Category": "Amazon",
    "Product Name": "100PCS Magnetic Tiles STEM Building Toys Set with 2 Cars, Sensory Stacking Magnetic Blocks for Toddlers & Kids, Ideal for Preschool Montessori Toys Christmas Birthday Gifts for Boys & Girls Ages 3+",
    "Product Image": "https://m.media-amazon.com/images/I/91UUewlD7BL._AC_SX679_.jpg",
    "Unique Key": "B0BVVF6V1S",
    "Clean URL": "https://www.amazon.com.au/Magnetic-Building-Preschool-Montessori-Christmas/dp/B0BVVF6V1S",
    "Brand": "Brand: Coodoo",
    "Average Star": "4.8 out of 5",
    "Reviews": [
        {
            "Date": "28 August 2024",
            "Stars": "4",
            "Review Text": "I don't usually write reviews, but this ine deserves one.\nMonths back i bought a knock off product (from another site), which were smaller tiles, only sides, and one magned per side. Recently my 5 year old started playing with them and really enjoyed it. I thought I'll upgrade, and it was the best decision! Blocks are amazing in a sense theatre you can build on top of each other without them toppling over! We'll, rest is upto your - *cough cough* I mean to your little one's imagination \ud83d\ude09\nOh, it even comes with small balconies for your castle!"
        },
        {
            "Date": "29 August 2024",
            "Stars": "5.0 out of 5 stars",
            "Review Text": "My son loves magnatiles but the packs are so small and pricey. These work the same, and he has so many more to play with! 10/10"
        }
    ]
}
    print(clean_transform_data(file))