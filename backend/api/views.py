from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import UserSerializer, ProductSumSerializer_HOME, SentimentDataSerializer_Dash, ProductSumSerializer_Dash, ProductSerializer_Dash
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, User_Products, Product_Summary, Product_Reviews, Product_Data_Source
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from scrape.scrapper import scrape_reviews, clean_url, get_site, is_valid_url
from ML.ReviewSumModel import summarize
from ML.sentiment import analyseSentiment, start_model
from Clean.Transform import clean_transform_data
from datetime import datetime, timedelta
import pandas as pd
from django.db import connection
from django.db.models import Q
import sys


#_____________________________________________________________________________________________________________________________
# USER Requests 

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
    
    


#_____________________________________________________________________________________________________________________________
# POST Requests 

class CreateProduct(APIView):
    
    permission_classes = [AllowAny]
    
    
    ### THINGS TO DO ###
    # - add user to user table p (tick)
    # - make functions for reoccuring parts (tick)
    # - check user aint already tracking it (tick)
    # - MEGA clean needed to code (eh)
    # if same link pasted twice (tick)
    
    def www(self, prod, rows):
        
        summary = summarize(rows)
        overview = summary.split('Overall:')[-1].replace('*', '').replace("\n", '')
        
        
        positive_count = len([ i[1] for i in rows if i[1] == 'Positive'])
        negative_count = len([ i[1] for i in rows if i[1] == 'Negative'])
        print(negative_count, positive_count, len(rows))
        
        if positive_count == 0:
            avg_pos = 0
        else:
            avg_pos = positive_count/len(rows)
            
        if negative_count == 0:
            avg_neg = 0
        else:
            avg_neg = negative_count/len(rows)
            
        avg_sentiment = round( avg_pos - avg_neg, 2)
        
        ratings = [ i[2] for i in rows ]
        avg_rating = sum(ratings)/len(ratings)
        
        prod_sum = Product_Summary(product=prod, summary=summary, overview=overview, avg_sentiment=avg_sentiment, avg_rating=avg_rating, review_count=len(rows), \
                postive_count=positive_count, negative_count=negative_count)
        prod_sum.save()
        
        serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=prod), many=True)
        
        return serializer
            
    def ddd(self, url):
        
        scraped = (scrape_reviews(url[0]))  
        cleaned = clean_transform_data(scraped)
        sent_model = start_model()
        
        product_meta = [cleaned['Product Name'], cleaned['Brand'], cleaned['Product Image']]
        
        for review in cleaned['Reviews']:
        
            # Sentiment
            sentiment = analyseSentiment(sent_model, review['Review Text']) 
            prod_rev = Product_Reviews(unique_code=scraped['Unique Key'], review=review['Review Text'], \
                sentiment=sentiment['score'], sentiment_label=sentiment['label'], rating=review['Stars'], date=review['Date'] )
            prod_rev.save()
            
        return product_meta
        
        
    def post(self, request): 
        
        # get and clean links to match up
        links = self.request.data['url']  
        links = [link for link in links if link != '' ]
        cleaned_urls = [clean_url(link) for link in links]
        cleaned_urls = set(cleaned_urls)
        print(cleaned_urls)
        
        # check links are valid
        for url in cleaned_urls:
            if (get_site(url[0]) is None) or (is_valid_url(url[0]) is False):
                print('broken link')
                return Response(status=status.HTTP_400_BAD_REQUEST)
         
        # get unique_code tuple 
        cleaned_links = [link[1] for link in cleaned_urls]
        
        if len(cleaned_links) == 1:
            cleaned_links = tuple([cleaned_links[0], ''])
            length = 1
        else:
            cleaned_links = tuple(cleaned_links)
            length = len(cleaned_links)
        
        print('here:', cleaned_links)
        # check if product exists
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT product_id, count(unique_code) 
                            FROM api_product_data_source 
                            WHERE unique_code IN {0}
                            GROUP BY product_id
                            """.format(cleaned_links))
            row = cursor.fetchall() 
            
        # check if product exists
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT product_id, count(unique_code) 
                            FROM api_product_data_source 
                            WHERE unique_code IN {0}
                            GROUP BY product_id
                            HAVING count(unique_code) = {1} 
                            """.format(cleaned_links, length))
            prods = cursor.fetchall() 
        
            # product exists
            if len(prods) > 0:
                print('product exists!!\n Product: %s' % row[0][0])
                
                product_id = prods[0][0]
                
                if User_Products.objects.filter(user=self.request.user, product=Product.objects.get(id=product_id)).exists():
                    print('User Already tracking')
                    return Response(status.HTTP_208_ALREADY_REPORTED)
                
                user_prod = User_Products(user=self.request.user, product=Product.objects.get(id=product_id))
                user_prod.save()
                
                serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=Product.objects.get(id=product_id)), many=True)
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)  
            
            else:
                print('product does not exist')
                
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT unique_code
                            FROM api_product_data_source 
                            WHERE unique_code IN {0}
                            """.format(cleaned_links))
                    rows = cursor.fetchall() 
                
                existing_links = [row[0] for row in rows]  
                product_meta =  [] 
                
                for link in cleaned_urls:
                    if link[1] not in existing_links:
                        product_meta  = self.ddd(link)
                    
                
                if len(product_meta) == 0:
                 with connection.cursor() as cursor:
                    cursor.execute("""
                                    SELECT DISTINCT name, brand, image
                                    FROM api_product_data_source ds
                                    INNER JOIN api_product p
                                    ON ds.product_id = p.id
                                    WHERE source = %s
                                    """, [link[0]])
                    product_meta = cursor.fetchone()
                
            
                # create table instances
                prod = Product(name=product_meta[0], brand=product_meta[1], image=product_meta[2])
                prod.save()
            
                user_prod = User_Products(user=self.request.user, product=prod)
                user_prod.save()
            
                for link in cleaned_urls:
                    link = Product_Data_Source(source=link[0], unique_code=link[1], product=prod, date=datetime.now())
                    link.save()

                with connection.cursor() as cursor:
                    cursor.execute("""
                                SELECT review, sentiment_label, rating
                                FROM api_product_reviews
                                WHERE unique_code IN {0}
                                    """.format(cleaned_links))
                    rows = cursor.fetchall() 
                
                serializer = self.www(prod, rows)
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
        print(product_id)
        
        with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT DISTINCT unique_code
                            FROM api_product_data_source
                            WHERE product_id = %s
                            """, [product_id])
                unique_codes = cursor.fetchall() 
        
        print(unique_codes)
        unique_codes = [uni_code[0] for uni_code in unique_codes]
        
    
        serializer = SentimentDataSerializer_Dash(Product_Reviews.objects.filter(unique_code__in=unique_codes), many=True)
        
        print(serializer.data)
    
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

# class ProductDelete(APIView):
    
#     permission_classes  = [IsAuthenticated]
    
#     def delete(self, request, product_id):

#         # Delete for user table, not whole product
#         User_Products.objects.filter(user=self.request.user,product=product_id).delete()
        
#         # Delete product if no user is tracking (no point storing irrelevant data)
#         if User_Products.objects.filter(product=product_id).exists() == False:
#             Product.objects.filter(pk=product_id).delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)


class ProductDelete(APIView):
    
    permission_classes  = [AllowAny]
    
    def delete(self, request, product_id):

        # Delete for user table, not whole product
        # User_Products.objects.filter(user=self.request.user,product=product_id).delete()
        User_Products.objects.filter(user=User.objects.get(id=2),product=product_id).delete()
        
        # Delete product if no user is tracking (no point storing irrelevant data)
        if User_Products.objects.filter(product=product_id).exists() == False:
            
            
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT DISTINCT unique_code
                            FROM api_product_data_source 
                            WHERE product_id = %s
                            """, [product_id])
                unique_codes = cursor.fetchall()
                
            Product.objects.filter(pk=product_id).delete()
                
            for unique_code in unique_codes:
                if Product_Data_Source.objects.filter(unique_code=unique_code[0]).exists() == False:
                    Product_Reviews.objects.filter(unique_code=unique_code[0]).delete()
            

        return Response(status=status.HTTP_204_NO_CONTENT)
     
