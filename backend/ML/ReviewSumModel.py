import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import nltk



# Notes:
# may need to add a timer for query try blocks for testing (so no  infinite loops)
# turn some of the code into functions as they repeat (completed)

def start_gemini():
    '''
    Starts gemini model
    '''
    
    gemini_api_key = 'AIzaSyAvnMQswSitVo9CWxP_Rhshwkii4dl0t-8'
    genai.configure(api_key = gemini_api_key)
    

    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    
    safety_config = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings = safety_config
        # See https://ai.google.dev/gemini-api/docs/safety-settings
        )
    
    return model



def batch_summary(model, query_revs):
    """ summarises reviews of a product.

    Args:
        model (gemini model): configuration of gemini model
        query_revs (list): list of product reviews

    Returns:
        str: summary of reviews (output of gemini)
    """
    
    # turn reviews list into str, split by ||
    query_str = ' || '.join(query_revs)
            
    # try gemini query until successful
    fail_counter = 0
    while True:
        try:
            batch_sum = model.generate_content(f"Can you please summarise these reviews for me, I want to understand what customers like and do not like about the product, the reviews are seperated by '||': {query_str}. Can you give the review summary with this format: Likes:, Dislikes: and Overall:. Make sure the Overall section is only a sentence (max 200 characters).")
            break
        except:
            if fail_counter == 4:
                print('ERROR: summarization is crashed...')
                return ''
            else:
                fail_counter += 1
                continue
        
    return batch_sum.text
    

def summarize(reviews):
    """Takes reviews of a product and outputs the overall summary of all the reviews

    Args:
        reviews (df): dataframe of review data

    Returns:
        str: overall summary of product
    """
    
    model = start_gemini()
    
    
    token_count = 0
    query_revs = []
    batch_sums = []
    
    # made for All_Beauty.json atm
    ##for review in reviews['reviewText']:
    for review in reviews:
        review = review[0]
        
        # get token count
        tokens = nltk.word_tokenize(review)
        token_count += len(tokens)
        print()
    
        # check if token count over the limit when review tokens added
        if token_count >= 1000000: # actual limit is (1,048,576)
            
            # try gemini query until successful
            batch_sums.append(batch_summary(model, query_revs))
                 
            token_count = len(tokens)
            query_revs = []
        
        query_revs.append(review)
    
    # final prod sum queried
    batch_sums.append(batch_summary(model, query_revs))
    
    # output the product summary
    if len(batch_sums) > 1:
        
        # if multiple summaries are made for a product, combine them
        query_sum = ' || '.join(batch_sums)
        fail_counter = 0
        while True:
            try:
                prod_sum = model.generate_content(f"Can you please combine these summarises for me, I want to understand what customers like and do not like about the product, the summaries are seperated by '||': {query_sum} . Can you give the review summary with this format: Likes:, Dislikes: and Overall:. Make sure the Overall section is only a sentence (max 200 characters).")
                break
            except:
                if fail_counter == 4:
                    print('ERROR: batch summarization failed...')
                    return ''
                else:
                    fail_counter += 1
                    continue
        
        return prod_sum.text
                
    else:
        return batch_sums[0]
            
        
        
if __name__ == '__main__':
    """ 
    Tests review summary function
    """
    #print('testing model...')
    
    ##df = pd.read_csv('/Users/gillyrosic/Downloads/Gemini_stuff/data/test_data.csv')
    ##df = df.rename(columns={"reviews.text": "reviewText"})
    ##print(summarize(df[df['asins']=="B00QJDU3KY"][['asins', 'reviewText']]))
    
    #review_dict = get_review_dict()
    #review_list = []

    #for i,v in review_dict.items():
        #review_list += v
    
    #print(summarize(review_list))