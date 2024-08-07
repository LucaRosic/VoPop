from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import UserSerializer, ProductSerializer, UserProductSerializer, ProductSumSerializer_HOME, SentimentDataSerializer_Dash, ProductSumSerializer_Dash, ProductSerializer_Dash
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, User_Products, Product_Summary, Product_Reviews
from rest_framework.response import Response
from rest_framework.views import APIView
from scrape.scrapper import scrape_reviews
from ML.ReviewSumModel import summarize
from ML.sentiment import analyseSentiment, start_model
import datetime
import nltk 

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    
    # make sure user does not already exist
    queryset = User.objects.all()
    
    # what we need to make user
    serializer_class = UserSerializer
    
    # who can make this view
    permission_classes = [AllowAny]
    
    
    
class CreateProductView(generics.ListCreateAPIView):
    
    queryset = Product.objects.all()
    
    serializer_class = ProductSerializer
    
    permission_classes = [AllowAny]
    
    # creates everything 
    def perform_create(self, serializer):
        
        if serializer.is_valid():
            # elt here
            
            # If product is already in database, only add to user_product table
            if Product.objects.filter(url=serializer.validated_data['url']).exists():
                
                if User_Products.objects.filter(user=User.objects.get(pk=2), product=Product.objects.get(url=serializer.validated_data['url'])).exists():
                    return  Response(status=status.HTTP_406_NOT_ACCEPTABLE)
                
                user_prod = User_Products(user=User.objects.get(pk=1), product=Product.objects.get(url=serializer.validated_data['url']))
                user_prod.save()
                serializer = ProductSerializer(Product.objects.get(url=serializer.validated_data['url']))
                return Response(data=serializer.data, status=status.HTTP_100_CONTINUE)
            else:
                #scrape data 
                scraped = (scrape_reviews(serializer.validated_data['url']))  
                
                # add to product table          
                serializer.save(name=scraped['Product Name'], category='amazon', brand=scraped['Brand'], image=scraped['Product Image'])
                # adds to user_product table
                user_prod = User_Products(user=User.objects.get(pk=2), product=Product.objects.get(pk=serializer.data['id']))
                
                # adds to product summary table
                user_prod.save()
                
                avg_sentiment = 0
                avg_rating = 0
                month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
                sent_model = start_model()
                for review in scraped['Reviews']:
                    
                    date = review['Date'].split('on ')[-1].split(' ')
                    sentiment = analyseSentiment(sent_model, review['Review Text'])
                    rating = float(review['Stars'].split(' ')[0])
                    avg_rating += rating
                    avg_sentiment += sentiment
                    if sentiment >= 0.5:
                        sentiment_label = 'Positive'
                    elif sentiment <= -0.5:
                        sentiment_label = 'Negative'
                    else: 
                        sentiment_label = 'Neutral'
                    
                    if date[0].isdigit():
                        prod_rev = Product_Reviews(product=Product.objects.get(pk=serializer.data['id']), review=review['Review Text'], \
                            sentiment=sentiment, sentiment_label=sentiment_label, rating=rating, date=datetime.date(int(date[-1]), month_dict[date[1]], int(date[0])))
                    else:
                        prod_rev = Product_Reviews(product=Product.objects.get(pk=serializer.data['id']), review=review['Review Text'], \
                            sentiment=sentiment, sentiment_label=sentiment_label, rating=rating, date=datetime.date(int(date[-1]), month_dict[date[0]], int(date[1].replace(',',''))))
                    prod_rev.save()
                    
                avg_sentiment = round(avg_sentiment/len(scraped['Reviews']),2)
                avg_rating = round(avg_rating/len(scraped['Reviews']),2)
                prod_sum = Product_Summary(product=Product.objects.get(pk=serializer.data['id']), summary=summarize(scraped['Reviews']), avg_sentiment=avg_sentiment, avg_rating=avg_rating)
                prod_sum.save()
                
        else:
            print(serializer.errors)

class ListUserProduct(generics.ListCreateAPIView):
    
    serializer_class = UserProductSerializer
    
    permission_classes = [AllowAny]
    
    queryset = User_Products.objects.all()

class DeleteUserProduct(generics.DestroyAPIView):
    
    queryset = User_Products.objects.all()
    
    permission_classes = [AllowAny]
    
    
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
        
   
class GetProduct_Meta_Dash(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, product_id):
                
        serializer = ProductSerializer_Dash(Product.objects.filter(pk=product_id), many=True)
        
        return Response(serializer.data)

class GetProductSum_Dash(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, product_id):
                
        serializer = ProductSumSerializer_Dash(Product_Summary.objects.filter(product=product_id), many=True)
        
        return Response(serializer.data)
    

    
   
        
                               
        
        
