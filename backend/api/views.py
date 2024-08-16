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
from Clean.Transform import clean_transform_data
import datetime



# Create your views here.
class CreateUserView(generics.CreateAPIView):
    
    # make sure user does not already exist
    queryset = User.objects.all()
    
    # what we need to make user
    serializer_class = UserSerializer
    
    # who can make this view
    permission_classes = [AllowAny]
    
    
    
class CreateProduct(generics.CreateAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    # creates everything 
    def perform_create(self, serializer):
        
        if serializer.is_valid():
            
            # If product is already in database, only add to user_product table
            if Product.objects.filter(url=serializer.validated_data['url']).exists():
                
                if User_Products.objects.filter(user=User.objects.get(pk=self.request.user), product=Product.objects.get(url=serializer.validated_data['url'])).exists():
                    return  Response(status=status.HTTP_406_NOT_ACCEPTABLE)
                
                user_prod = User_Products(user=User.objects.get(pk=1), product=Product.objects.get(url=serializer.validated_data['url']))
                user_prod.save()
                serializer = ProductSerializer(Product.objects.get(url=serializer.validated_data['url']))
                return Response(data=serializer.data, status=status.HTTP_100_CONTINUE)
            
            else:
                # scrape and clean data 
                scraped = (scrape_reviews(serializer.validated_data['url']))  
                
                if scraped is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                
                cleaned = clean_transform_data(scraped)
                
                
                # add to product table          
                serializer.save(name=scraped['Product Name'], category='amazon', brand=scraped['Brand'], image=scraped['Product Image'])
                
                # adds to user_product table
                user_prod = User_Products(user=User.objects.get(pk=self.request.user), product=Product.objects.get(pk=serializer.data['id']))
                user_prod.save() 
                
                avg_sentiment = 0
                avg_rating = 0
                ##month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
                sent_model = start_model()
                for review in cleaned['Reviews']:
                    
                    avg_rating += review['Stars']
                    
                    ##date = review['Date'].split('on ')[-1].split(' ')
                    ##rating = float(review['Stars'].split(' ')[0])
                    ##avg_rating += rating
                    
                    sentiment = analyseSentiment(sent_model, review['Review Text'])
                    avg_sentiment += sentiment['score']
                    
                        
                    prod_rev = Product_Reviews(product=Product.objects.get(pk=serializer.data['id']), review=review['Review Text'], \
                        sentiment=sentiment['score'], sentiment_label=sentiment['label'], rating=review['Stars'], date=review['Date'] )
                    
                    # if date[0].isdigit():
                    #     prod_rev = Product_Reviews(product=Product.objects.get(pk=serializer.data['id']), review=review['Review Text'], \
                    #         sentiment=sentiment['score'], sentiment_label=sentiment['label'], rating=rating, date=datetime.date(int(date[-1]), month_dict[date[1]], int(date[0])) )
                    # else:
                    #     prod_rev = Product_Reviews(product=Product.objects.get(pk=serializer.data['id']), review=review['Review Text'], \
                    #         sentiment=sentiment['score'], sentiment_label=sentiment['label'], rating=rating, date=datetime.date(int(date[-1]), month_dict[date[0]], int(date[1].replace(',',''))))
                    
                    prod_rev.save()
                    
                avg_sentiment = round(avg_sentiment/len(cleaned['Reviews']),2)
                avg_rating = round(avg_rating/len(cleaned['Reviews']),2)
                summary=summarize(scraped['Reviews'])
                overview = summary.split('Overall:')[-1].replace('*', '').replace('\n', '')
                
                prod_sum = Product_Summary(product=Product.objects.get(pk=serializer.data['id']), summary=summary, overview=overview, avg_sentiment=avg_sentiment, avg_rating=avg_rating)
                prod_sum.save()
                
        else:
            print(serializer.errors)
    
    
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
    
    permission_classes  = [IsAuthenticated]
    
    def get(self, request, product_id):
        
        serializer = SentimentDataSerializer_Dash(Product_Reviews.objects.filter(product=product_id), many=True)
        
        return Response(serializer.data)
        
   
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
    
