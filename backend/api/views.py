from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
<<<<<<< HEAD
from .serializers import UserSerializer, ProductSerializer, UserProductSerializer, ProductSumSerializer_HOME, SentimentDataSerializer_Dash, ProductSumSerializer_Dash, ProductSerializer_Dash
=======
from .serializers import UserSerializer, ProductSumSerializer_HOME, SentimentDataSerializer_Dash, ProductSumSerializer_Dash, ProductSerializer_Dash
>>>>>>> Dev
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, User_Products, Product_Summary, Product_Reviews
from rest_framework.response import Response
from rest_framework.views import APIView
<<<<<<< HEAD
from scrape.scrapper import scrape_reviews
from ML.ReviewSumModel import summarize
from ML.sentiment import analyseSentiment, start_model
from Clean.Transform import clean_transform_data
import datetime
import nltk 
=======
from rest_framework_simplejwt.tokens import RefreshToken
from scrape.scrapper import scrape_reviews, clean_url
from ML.ReviewSumModel import summarize
from ML.sentiment import analyseSentiment, start_model
from Clean.Transform import clean_transform_data
from datetime import datetime, timedelta
import pandas as pd


#_____________________________________________________________________________________________________________________________
# USER Requests 
>>>>>>> Dev

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    
    # make sure user does not already exist
    queryset = User.objects.all()
    
    # what we need to make user
    serializer_class = UserSerializer
    
    # who can make this view
    permission_classes = [AllowAny]
    
    
    
<<<<<<< HEAD
class CreateProduct(generics.ListCreateAPIView):
=======
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)  
>>>>>>> Dev
    
    


#_____________________________________________________________________________________________________________________________
# POST Requests 

class CreateProduct(APIView):
    
    permission_classes = [IsAuthenticated]
    
<<<<<<< HEAD
    # creates everything 
    def perform_create(self, serializer):
        
        if serializer.is_valid():
            
            # If product is already in database, only add to user_product table
            if Product.objects.filter(url=serializer.validated_data['url']).exists():
                
                if User_Products.objects.filter(user=User.objects.get(pk=2), product=Product.objects.get(url=serializer.validated_data['url'])).exists():
                    return  Response(status=status.HTTP_406_NOT_ACCEPTABLE)
                
                user_prod = User_Products(user=User.objects.get(pk=1), product=Product.objects.get(url=serializer.validated_data['url']))
                user_prod.save()
                serializer = ProductSerializer(Product.objects.get(url=serializer.validated_data['url']))
                return Response(data=serializer.data, status=status.HTTP_100_CONTINUE)
            else:
                # scrape and clean data 
                scraped = (scrape_reviews(serializer.validated_data['url']))  
                cleaned = clean_transform_data(scraped)
                
                # add to product table          
                serializer.save(name=scraped['Product Name'], category='amazon', brand=cleaned['Brand'], image=cleaned['Product Image'])
                
                # adds to user_product table
                user_prod = User_Products(user=User.objects.get(pk=2), product=Product.objects.get(pk=serializer.data['id']))
                user_prod.save() 
                
                avg_sentiment = 0
                avg_rating = 0
                ##month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
                sent_model = start_model()
                for review in cleaned['Reviews']:
                    
                    # date = review['Date'].split('on ')[-1].split(' ')
                    sentiment = analyseSentiment(sent_model, review['Review Text'])
                    # rating = float(review['Stars'].split(' ')[0])
                    avg_rating += review['Stars']
                    avg_sentiment += sentiment
                    if sentiment >= 0.5:
                        sentiment_label = 'Positive'
                    elif sentiment <= -0.5:
                        sentiment_label = 'Negative'
                    else: 
                        sentiment_label = 'Neutral'
                    
                    # if date[0].isdigit():
                    prod_rev = Product_Reviews(product=Product.objects.get(pk=serializer.data['id']), review=review['Review Text'], \
                        sentiment=sentiment, sentiment_label=sentiment_label, rating=review['Stars'], date=datetime.date(review['Date'][-1], review['Date'][1], review['Date'][0]) )
                    # else:
                    #     prod_rev = Product_Reviews(product=Product.objects.get(pk=serializer.data['id']), review=review['Review Text'], \
                    #         sentiment=sentiment, sentiment_label=sentiment_label, rating=rating, date=datetime.date(int(date[-1]), month_dict[date[0]], int(date[1].replace(',',''))))
                    prod_rev.save()
                    
                avg_sentiment = round(avg_sentiment/len(cleaned['Reviews']),2)
                avg_rating = round(avg_rating/len(cleaned['Reviews']),2)
                prod_sum = Product_Summary(product=Product.objects.get(pk=serializer.data['id']), summary=summarize(cleaned['Reviews']), avg_sentiment=avg_sentiment, avg_rating=avg_rating)
                prod_sum.save()
                
=======
    def post(self, request):
        
        # Check if product is in DB
        cleaned_url, unique_code = clean_url(request.data['url'])
        
        # Product is already in database
        if Product.objects.filter(unique_code=unique_code).exists():
            
            # User is already tracking product
            if User_Products.objects.filter(user=self.request.user, product=Product.objects.get(url=cleaned_url)).exists():
                return Response(status=status.HTTP_208_ALREADY_REPORTED)
            
            
            # Connect product to user
            user_prod = User_Products(user=request.user, product=Product.objects.get(unique_code=unique_code))
            user_prod.save()
            
            
            # Return Product card details to frontend
            serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=Product.objects.get(unique_code=unique_code)), many=True)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        
>>>>>>> Dev
        else:
            
            # scrape data
            scraped = (scrape_reviews(request.data['url']))  
            
            
            # URL link is invalid
            if scraped is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            
            # Clean scraped data
            cleaned = clean_transform_data(scraped)
            
            # Add to product table  
            prod = Product(name=scraped['Product Name'], url=scraped['Clean URL'], unique_code=scraped['Unique Key'], category=scraped['Category'], brand=scraped['Brand'], image=scraped['Product Image'])        
            prod.save()
            
            # Connects Product to User
            user_prod = User_Products(user=request.user, product=Product.objects.get(unique_code=scraped['Unique Key']))
            user_prod.save() 
            
            
            
            postive_count = 0
            negative_count = 0
            sent_model = start_model()
            
            for review in cleaned['Reviews']:
                
                # Sentiment
                sentiment = analyseSentiment(sent_model, review['Review Text'])
                
                # Count positive and negative reviews
                if sentiment['label'] == 'Positive':
                    postive_count += 1
                elif sentiment['label'] == 'Negative':
                    negative_count += 1
                
                
                # Add product reviews
                prod_rev = Product_Reviews(product=Product.objects.get(unique_code=scraped['Unique Key']), review=review['Review Text'], \
                    sentiment=sentiment['score'], sentiment_label=sentiment['label'], rating=review['Stars'], date=review['Date'] )
                prod_rev.save()
                   
            # Calculate avg. sentiment (NPS) for Product       
            avg_sentiment = round( (postive_count/len(cleaned['Reviews'])) - (negative_count/len(cleaned['Reviews']) ) ,2)
            
            # Gemini Review Summary Model
            summary=summarize(scraped['Reviews'])
            
            # Overivew for frontend product cards
            overview = summary.split('Overall:')[-1].replace('*', '').replace("\n", '')
            
            # avg_rating = float(scraped['Average Star'].split(' ')[0])
            
            
            # Add product summary
            prod_sum = Product_Summary(product=Product.objects.get(unique_code=scraped['Unique Key']), summary=summary, overview=overview, avg_sentiment=avg_sentiment, review_count=len(cleaned['Reviews']), \
                postive_count=postive_count, negative_count=negative_count, avg_rating=cleaned['Average Stars'])
            prod_sum.save()
            
            # Return product card data to frontend
            serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=Product.objects.get(unique_code=scraped['Unique Key'])), many=True)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
    
    

#__________________________________________________________________________________________________________________________
# GET Requests

# INFO FOR HOME
class GetUserProduct_Home(generics.ListAPIView):
    
    serializer_class = ProductSumSerializer_HOME
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        
        product_ids = User_Products.objects.filter(user=self.request.user).values_list('product', flat=True)
                
        return Product_Summary.objects.filter(product__in=product_ids)
    

# INFO FOR DASH
class GetReviewSent_Dash(APIView):
    
    permission_classes  = [AllowAny]
    
    def get(self, request, product_id):
        
        serializer = SentimentDataSerializer_Dash(Product_Reviews.objects.filter(product=product_id), many=True)
        datalist = pd.DataFrame(serializer.data)
        datalist['date'] = pd.to_datetime(datalist['date'], yearfirst=True)
        datalist['month'] = datalist['date'].dt.month
        last_year = datetime.now() - timedelta(days=365)
        filtered_datalist = datalist.loc[datalist['date'] > last_year]
        agg_datalist = filtered_datalist.groupby(['month','sentiment_label'])['sentiment_label'].count().reset_index(name='sentiment_count')
        chart_data = [[0]*12 for num in range(3)]

        for index, row in agg_datalist.iterrows():
            if row['sentiment_label'] == 'Positive':
                chart_data[0][row['month']-1] = row['sentiment_count']
            elif row['sentiment_label'] == 'Negative':
                chart_data[1][row['month']-1] = row['sentiment_count']
            else:
                chart_data[2][row['month']-1] = row['sentiment_count']    
        return Response(chart_data)
        
   
class GetProductMeta_Dash(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, product_id):
                
        serializer = ProductSerializer_Dash(Product.objects.filter(pk=product_id), many=True)
        
        return Response(serializer.data)


class GetProductSum_Dash(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, product_id):
                
        serializer = ProductSumSerializer_Dash(Product_Summary.objects.filter(product=product_id), many=True)
        
        return Response(serializer.data)
      
class GetNewRewreviews(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        url = request.GET.get('url')
        date = request.GET.get('date')
        return Response(scrape_reviews(url,date))

class GetSentimentNewReviews(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        sent_model = start_model()
        review = request.GET.get('review')
        return Response(analyseSentiment(sent_model, review))
  
#_____________________________________________________________________________________________________________________________
# DELETE Requests  

class ProductDelete(APIView):
    
<<<<<<< HEAD
    
class GetProds(generics.RetrieveAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    
class GetUProds(generics.RetrieveAPIView):
    
    lookup_field = 'product_id'
    queryset = User_Products.objects.all()
    serializer_class = UserProductSerializer
    permission_classes = [AllowAny]
    
#_____________________________________________________________________________________________________________________________
# POST Stuff

## most promising so far    
class GetProductDetails(APIView):
    
    permission_classes  = [AllowAny]
    
    def get(self, request, product_id):
        
        serializer = ProductSerializer(Product.objects.filter(id=product_id), many=True)
        
        print(serializer.data[0]['url'])
        
        return Response(serializer.data)
    
    def delete(self, request, product_id):

        # delete for user table, not whole product
        Product.objects.filter(id=product_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

## GET STUFF

# WORKING REQUESTS
#__________________________________________________________________________________________________________________________
# INFO FOR HOME
class GetUserProduct_HomePage(generics.ListAPIView):
    serializer_class = ProductSumSerializer_HOME
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        
        product_ids = User_Products.objects.filter(user=self.request.user).values_list('product', flat=True)
                
        return Product_Summary.objects.filter(product__in=product_ids)
    

# INFO FOR DASH
class GetReviewSent_Dash(APIView):
    
    permission_classes  = [AllowAny]
    
    def get(self, request, product_id):
        
        serializer = SentimentDataSerializer_Dash(Product_Reviews.objects.filter(product=product_id), many=True)
        
        return Response(serializer.data)
        
   
class GetProductMeta_Dash(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, product_id):
                
        serializer = ProductSerializer_Dash(Product.objects.filter(pk=product_id), many=True)
        
        return Response(serializer.data)

class GetProductSum_Dash(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, product_id):
                
        serializer = ProductSumSerializer_Dash(Product_Summary.objects.filter(product=product_id), many=True)
        
        return Response(serializer.data)
    

    
   
        
                               
        
        
=======
    permission_classes  = [IsAuthenticated]
    
    def delete(self, request, product_id):

        # Delete for user table, not whole product
        User_Products.objects.filter(user=self.request.user,product=product_id).delete()
        
        # Delete product if no user is tracking (no point storing irrelevant data)
        if User_Products.objects.filter(product=product_id).exists() == False:
            Product.objects.filter(pk=product_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
     
>>>>>>> Dev
