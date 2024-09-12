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
    # - add user to user table p
    # - make functions for reoccuring parts 
    # - check user aint already tracking it
    # - MEGA clean needed to code 
    # if same link pasted twice (move to link link  situation)
    
    def www(self, prod, rows):
        
        summary = summarize(rows)
        overview = summary.split('Overall:')[-1].replace('*', '').replace("\n", '')
        
        positive_count = len([ i[1] for i in rows if i[1] == 'Positive'])
        negative_count = len([ i[1] for i in rows if i[1] == 'Negative'])
        avg_sentiment = round( (positive_count/len(rows)) - (negative_count/len(rows) ) ,2)
        
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
        
        if len(request.data) == 2:
            
            # clean urls and get unique code     
            clean_urls = [clean_url(url) for url in request.data.values()]
            
            
            # check links are valid 
            for i in clean_urls:
                if get_site(i[0]) is None:
                    print('here1')
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                
                if is_valid_url(i[0]) is False:
                    print('here2')
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                    
            
            # checking if product is in db            
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT ds1.product_id as product_id, ds1.source as source_1, ds2.source as source_2 
                                FROM api_product_data_source ds1, api_product_data_source ds2 
                                Where ds1.product_id = ds2.product_id 
                                AND ds1.id != ds2.id
                                AND ds1.source = %s 
                                AND ds2.source = %s""", [clean_urls[0][0], clean_urls[1][0]])
                row = cursor.fetchall()   
            
            # product exists
            if len(row) == 1:
                product_id = row[0][0]
                #user_prod = User_Products(user=self.request.user, product=Product.objects.get(id=product_id))
                if User_Products.objects.filter(user=User.objects.get(id=2), product=Product.objects.get(id=product_id)).exists():
                    return Response(status.HTTP_208_ALREADY_REPORTED)
                
                user_prod = User_Products(user=User.objects.get(id=2), product=Product.objects.get(id=product_id))
                
                user_prod.save()
                serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=Product.objects.get(id=product_id)), many=True)
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            
            # check if url links are in db
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT DISTINCT source
                            FROM api_product_data_source
                            WHERE source = %s
                            OR source = %s""", [clean_urls[0][0], clean_urls[1][0]])
                rows = cursor.fetchall()   
            
            
            existing_links = [row[0] for row in rows]    
            product_meta =  [] 
            
            print(existing_links)           
            
            for url in clean_urls:
                
                # scrape link and add reviews to db if link not in db
                if url[0] not in existing_links:
                    print('not in:', url)
                    
                    product_meta  = self.ddd(url)
                    
                        
                        
            if len(product_meta) == 0:
                with connection.cursor() as cursor:
                    cursor.execute("""
                                SELECT DISTINCT name, brand, image
                                FROM api_product_data_source ds
                                INNER JOIN api_product p
                                ON ds.product_id = p.id
                                WHERE source = %s
                                """, [cleaned_url[0]])
                    product_meta = cursor.fetchone()
                
            
            # create table instances
            prod = Product(name=product_meta[0], brand=product_meta[1], image=product_meta[2])
            prod.save()
            
            user_prod = User_Products(user=User.objects.get(id=2), product=prod)
            user_prod.save()
            
            link1 = Product_Data_Source(source=clean_urls[0][0], unique_code=clean_urls[0][1], product=prod, date=datetime.now())
            link1.save()
            
            link2 = Product_Data_Source(source=clean_urls[1][0], unique_code=clean_urls[1][1], product=prod, date=datetime.now())
            link2.save()
            
            # collect all reviews for product
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT review, sentiment_label, rating
                            FROM api_product_reviews
                            WHERE unique_code = %s
                            OR unique_code = %s""", [clean_urls[0][1], clean_urls[1][1]])
                rows = cursor.fetchall()  
            
            
            
            # create product summary instance  
            
            serializer = self.www(prod, rows)
            
            
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)

        
        #________________________________________________________________________________________
        
        
        
        ### 1 link given
        else:
            
            # get unicdoe and clean url
            cleaned_url  = clean_url(request.data['url1'])
            
            # check link is valid (combine into one if) 
            if get_site(cleaned_url[0]) is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
                
            if is_valid_url(cleaned_url[0]) is False:
                return Response(status=status.HTTP_400_BAD_REQUEST) 
            
            
            # check if product exists already 
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT Distinct ds1.product_id 
                                FROM api_product_data_source ds1, api_product_data_source ds2 
                                Where ds1.product_id = ds2.product_id 
                                AND ds1.id != ds2.id
                                AND ds1.source = %s 
                                """, [cleaned_url[0]])
                prod_ids = cursor.fetchall()   
            
            print(prod_ids, cleaned_url[0])    
            for prod_id in prod_ids:
                with connection.cursor() as cursor:
                    cursor.execute("""
                                SELECT source 
                                    FROM api_product_data_source 
                                    Where product_id = %s 
                                    AND source != %s 
                                    """, [prod_id[0], cleaned_url[0]])
                    prod_exists = cursor.fetchall() 
                
                if len(prod_exists) == 0:
                    
                    if User_Products.objects.filter(user=User.objects.get(id=2), product=Product.objects.get(id=product_id)).exists():
                        return Response(status.HTTP_208_ALREADY_REPORTED)
                    
                    user_prod = User_Products(user=self.request.user, product=Product.objects.get(id=prod_id))
                    user_prod.save()
                    serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=Product.objects.get(id=prod_id)), many=True)
                    return Response(status.HTTP_208_ALREADY_REPORTED, data=serializer.data)
                    
            # check if link is in db (for combined link prod)
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT DISTINCT source
                            FROM api_product_data_source
                            WHERE source = %s
                            """, [cleaned_url[0]])
                row = cursor.fetchall()      
            
            # if not scrape
            if len(row) == 0:
                print('not in:', cleaned_url[0]) 
                product_meta  = self.ddd(cleaned_url)
            
            # if link in  db, just collect product meta data
            else:
                with connection.cursor() as cursor:
                    cursor.execute("""
                                SELECT DISTINCT name, brand, image
                                FROM api_product_data_source ds
                                INNER JOIN api_product p
                                ON ds.product_id = p.id
                                WHERE source = %s
                                """, [cleaned_url[0]])
                    product_meta = cursor.fetchone()
                
            
            # create table instances
            prod = Product(name=product_meta[0], brand=product_meta[1], image=product_meta[2])
            prod.save()
            
            user_prod = User_Products(user=User.objects.get(id=2), product=prod)
            user_prod.save() 
            
            link1 = Product_Data_Source(source=cleaned_url[0], unique_code=cleaned_url[1], product=prod, date=datetime.now())
            link1.save()   
            
            
            # collect all the reviews    
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT review, sentiment_label, rating
                            FROM api_product_reviews
                            WHERE unique_code = %s
                            """, [cleaned_url[1]])
                rows = cursor.fetchall()
            
            # create product summary instance, self.www(prod, rows)
            
            serializer = self.www(prod, rows) 
            
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        
        
            # scraped = (scrape_reviews(url[0]))  
                    # cleaned = clean_transform_data(scraped)
                    # sent_model = start_model()
                    
                    # product_meta = [cleaned['Product Name'], cleaned['Brand'], cleaned['Product Image']]
                    
                    # for review in cleaned['Reviews']:
                    
                    #     # Sentiment
                    #     sentiment = analyseSentiment(sent_model, review['Review Text']) 
                    #     prod_rev = Product_Reviews(unique_code=scraped['Unique Key'], review=review['Review Text'], \
                    #         sentiment=sentiment['score'], sentiment_label=sentiment['label'], rating=review['Stars'], date=review['Date'] )
                    #     prod_rev.save()
            
            #___________________#

            # summary = summarize(rows)
            # overview = summary.split('Overall:')[-1].replace('*', '').replace("\n", '')
            
            # positive_count = len([ i[1] for i in rows if i[1] == 'Positive'])
            # negative_count = len([ i[1] for i in rows if i[1] == 'Negative'])
            # avg_sentiment = round( (positive_count/len(rows)) - (negative_count/len(rows) ) ,2)
            
            # ratings = [ i[2] for i in rows ]
            # avg_rating = sum(ratings)/len(ratings)
            
            # prod_sum = Product_Summary(product=prod, summary=summary, overview=overview, avg_sentiment=avg_sentiment, avg_rating=avg_rating, review_count=len(rows), \
            #         postive_count=positive_count, negative_count=negative_count)
            # prod_sum.save()
            
            
            # serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=prod), many=True)
            
            
            #________________________________________________________________________________________________    
           

            # scraped = (scrape_reviews(cleaned_url[0]))  
            #     cleaned = clean_transform_data(scraped)
            #     sent_model = start_model()
                
            #     product_meta = [cleaned['Product Name'], cleaned['Brand'], cleaned['Product Image']]
                
            #     for review in cleaned['Reviews']:
                
            #         # Sentiment
            #         sentiment = analyseSentiment(sent_model, review['Review Text']) 
            #         prod_rev = Product_Reviews(unique_code=scraped['Unique Key'], review=review['Review Text'], \
            #             sentiment=sentiment['score'], sentiment_label=sentiment['label'], rating=review['Stars'], date=review['Date'] )
            #         prod_rev.save()
            
            #___________________#
            
            # summary = summarize(rows)
            # overview = summary.split('Overall:')[-1].replace('*', '').replace("\n", '')
            
            # positive_count = len([ i[1] for i in rows if i[1] == 'Positive'])
            # negative_count = len([ i[1] for i in rows if i[1] == 'Negative'])
            # avg_sentiment = round( (positive_count/len(rows)) - (negative_count/len(rows) ) ,2)
            
            # ratings = [ i[2] for i in rows ]
            # avg_rating = sum(ratings)/len(ratings)
            
            # prod_sum = Product_Summary(product=prod, summary=summary, overview=overview, avg_sentiment=avg_sentiment, avg_rating=avg_rating, review_count=len(rows), \
            #         postive_count=positive_count, negative_count=negative_count)
            # prod_sum.save()
            
            
            # serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=prod), many=True)
                
                    
        
    
    

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
        
        with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT DISTINCT unique_code
                            FROM api_product_data_source
                            WHERE product_id = %s
                            """, [product_id])
                unique_codes = cursor.fetchall() 
        
        print(unique_codes)
        
        if len(unique_codes) == 2:
            serializer = SentimentDataSerializer_Dash(Product_Reviews.objects.filter(Q(unique_code=unique_codes[0][0]) |  Q(unique_code=unique_codes[1][0])), many=True)
        else: 
            serializer = SentimentDataSerializer_Dash(Product_Reviews.objects.filter(unique_code=unique_codes[0][0]), many=True)
        
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
     
