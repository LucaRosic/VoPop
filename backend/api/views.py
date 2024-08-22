from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import UserSerializer, ProductSerializer, UserProductSerializer, ProductSumSerializer_HOME, SentimentDataSerializer_Dash, ProductSumSerializer_Dash, ProductSerializer_Dash
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, User_Products, Product_Summary, Product_Reviews
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from scrape.scrapper import scrape_reviews, clean_url
from ML.ReviewSumModel import summarize
from ML.sentiment import analyseSentiment, start_model
from Clean.Transform import clean_transform_data
from datetime import datetime, timedelta
import pandas as pd



# Create your views here.
class CreateUserView(generics.CreateAPIView):
    
    # make sure user does not already exist
    queryset = User.objects.all()
    
    # what we need to make user
    serializer_class = UserSerializer
    
    # who can make this view
    permission_classes = [AllowAny]
    
    
    
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
    
    

class CreateProduct(APIView):
    
    permission_classes = [IsAuthenticated]
    
    # creates everything 
    def post(self, request):
        
        cleaned_url = clean_url(request.data['url'])
        #print(cleaned_url)
        #cleaned_url, _ = clean_url(request.data['url'])
        
        
        # If product is already in database, only add to user_product table
        if Product.objects.filter(url=cleaned_url).exists():
            
            if User_Products.objects.filter(user=self.request.user, product=Product.objects.get(url=cleaned_url)).exists():
                return Response(status=status.HTTP_208_ALREADY_REPORTED)
            
            user_prod = User_Products(user=request.user, product=Product.objects.get(url=cleaned_url))
            user_prod.save()
            serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=Product.objects.get(url=cleaned_url)), many=True)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        
        else:
            
            scraped = (scrape_reviews(request.data['url']))  
            
            if scraped is None:
                
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            cleaned = clean_transform_data(scraped)
            
            
            # add to product table  
            prod = Product(name=scraped['Product Name'], url=scraped['Clean URL'], category=scraped['Category'], brand=scraped['Brand'], image=scraped['Product Image'])        
            prod.save()
            
            # adds to user_product table
            user_prod = User_Products(user=request.user, product=Product.objects.get(url=scraped['Clean URL']))
            user_prod.save() 
            
            avg_sentiment = 0
            sent_model = start_model()
            for review in cleaned['Reviews']:
                
                sentiment = analyseSentiment(sent_model, review['Review Text'])
                avg_sentiment += sentiment['score']
                
                prod_rev = Product_Reviews(product=Product.objects.get(url=scraped['Clean URL']), review=review['Review Text'], \
                    sentiment=sentiment['score'], sentiment_label=sentiment['label'], rating=review['Stars'], date=review['Date'] )
                
                
                prod_rev.save()
                
            avg_sentiment = round(avg_sentiment/len(cleaned['Reviews']),2)
            ##avg_rating = round(avg_rating/len(cleaned['Reviews']),2)
            summary=summarize(scraped['Reviews'])
            overview = summary.split('Overall:')[-1].replace('*', '').replace("\n", '')
            avg_rating = float(scraped['Average Star'].split(' ')[0])
                        
            prod_sum = Product_Summary(product=Product.objects.get(url=scraped['Clean URL']), summary=summary, overview=overview, avg_sentiment=avg_sentiment, avg_rating=avg_rating)
            prod_sum.save()
            
            
            serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=Product.objects.get(url=scraped['Clean URL'])), many=True)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
    
    
## DELETE USER_PRODUCT

#class DeleteProduct(APIView)   
#    def delete()    
    
## GET STUFF

# WORKING REQUESTS
#__________________________________________________________________________________________________________________________
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
      
      
      
#_____________________________________________________________________________________________________________________________
# POST Stuff

## most promising so far    
class GetProductDetails(APIView):
    
    permission_classes  = [IsAuthenticated]
    
    def get(self, request, product_id):
        
        serializer = ProductSerializer(Product.objects.filter(id=product_id), many=True)
        
        return Response(serializer.data)
    
    def delete(self, request, product_id):

        # delete for user table, not whole product
        User_Products.objects.filter(user=self.request.user,product=product_id).delete()
        
        if User_Products.objects.filter(product=product_id).exists() == False:
            Product.objects.filter(pk=product_id).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
     