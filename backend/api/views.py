from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from scrape.scrapper import scrape_reviews, clean_url, get_site, is_valid_url
from ML.ReviewSumModel import summarize
from ML.sentiment import analyseSentiment, start_model,analyseMultiple
from Clean.Transform import clean_transform_data
from datetime import datetime, timedelta
import pandas as pd
from django.db import connection

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
    
    permission_classes = [IsAuthenticated]
    
    
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
        #print(negative_count, positive_count, len(rows))
        
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
        
        if sum(ratings) == 0:
            avg_rating = 0
        else:
            avg_rating = sum(ratings)/len(ratings)
        
        prod_sum = Product_Summary(product=prod, summary=summary, overview=overview, avg_sentiment=avg_sentiment, avg_rating=avg_rating, review_count=len(rows), \
                positive_count=positive_count, negative_count=negative_count)
        prod_sum.save()
        
        serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=prod), many=True)
        
        return serializer
            
    def ddd(self, url):
        
        print()
        scraped = (scrape_reviews(url[0]))  
        print()
        print('cleaning data')
        cleaned = clean_transform_data(scraped)
        
        print('running sentiment analysis')
        print()
        sent_model = start_model()
        print()
        product_meta = [cleaned['Product Name'], cleaned['Brand'], cleaned['Product Image']]
        
        print('adding reviews to database')
        for review in cleaned['Reviews']:
            
            sentiment = analyseSentiment(sent_model, review['Review Text']) 
            
            if review['Stars'] == '' or review['Stars'] == None:
                prod_rev = Product_Reviews(unique_code=scraped['Unique Key'], review=review['Review Text'], \
                sentiment=sentiment['score'], sentiment_label=sentiment['label'], date=review['Date'] )
            
            else:
                prod_rev = Product_Reviews(unique_code=scraped['Unique Key'], review=review['Review Text'], \
                    sentiment=sentiment['score'], sentiment_label=sentiment['label'], rating=review['Stars'], date=review['Date'] )
            
            prod_rev.save()
        
        source_date = Source_date(source=url[0], date=datetime.now())
        source_date.save()
            
        return product_meta
        
        
    def post(self, request): 
        
        print('adding product...')
        # get and clean links to match up
        links = self.request.data['url']  
        links = [link for link in links if link != '' ]
        cleaned_urls = [clean_url(link) for link in links]
        cleaned_urls = set(cleaned_urls)
        
        
        # check links are valid
        print('checking links are valid...', end=' ')
        for url in cleaned_urls:
            if (get_site(url[0]) is None) or (is_valid_url(url[0]) is False):
                print('link not valid\n Exit')
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
        print('links are valid') 
        # get unique_code tuple 
        cleaned_links = [link[1] for link in cleaned_urls]
        
        if len(cleaned_links) == 1:
            cleaned_links = tuple([cleaned_links[0], cleaned_links[0]])
            length = 1
        else:
            cleaned_links = tuple(cleaned_links)
            length = len(cleaned_links)
        
        print('checking if product exists...', end=' ')
        # check if product exists
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT product_id, count(unique_code) 
                            FROM api_product_data_source 
                            WHERE unique_code IN {0}
                            GROUP BY product_id
                            HAVING count(unique_code) = {1}
                            """.format(cleaned_links, length))
            row = cursor.fetchall() 
            # this aint right, row into next query
        
        if len(row) != 0:
        
            prod_ids = [r[0] for r in row]    
            if len(prod_ids) == 1:
                prod_ids.append(prod_ids[0])
            prod_ids = tuple(prod_ids)
                    
            print('prods:', prod_ids)
            
            # check if product exists
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT product_id, count(unique_code) 
                                FROM api_product_data_source 
                                WHERE product_id IN {0}
                                GROUP BY product_id
                                HAVING count(unique_code) = {1} 
                                """.format(prod_ids, length))
                prods = cursor.fetchall() 
        
        else: 
            prods = []
            print('no prod in db exemption...', end=' ')
            
            
        # product exists
        if len(prods) > 0:
            print('product exists!!\n Product: %s' % prods[0][0])
            
            product_id = prods[0][0]
            
            if User_Products.objects.filter(user=self.request.user, product=Product.objects.get(id=product_id)).exists():
                print('User Already tracking\n Exit')
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
            
            print('checking if links exist in database...')
            for link in cleaned_urls:
                if link[1] not in existing_links:
                    print(link[1], 'not in database\n Scrapping link...')
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
            print('adding data to database...')
            
            print(' created product instance')
            prod = Product(name=product_meta[0], brand=product_meta[1], image=product_meta[2])
            prod.save()

            print(' created user_product instance')
            user_prod = User_Products(user=self.request.user, product=prod)
            user_prod.save()
        
            for link in cleaned_urls:
                print(' created data_source instance for', link[1])
                if 'amazon' in link[0]:
                    category = 'Amazon'
                elif 'aliexpress' in link[0]:
                    category = 'AliExpress'
                link = Product_Data_Source(source=link[0], unique_code=link[1], product=prod, category=category)
                link.save()

            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT review, sentiment_label, rating
                            FROM api_product_reviews
                            WHERE unique_code IN {0}
                                """.format(cleaned_links))
                rows = cursor.fetchall() 
            
            print(' creating summary instance')
            serializer = self.www(prod, rows)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)    


     
class AddLink(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):     
        
        print('adding link...')
        
        product_id = self.request.data['url'][0]
        url = self.request.data['url'][1]

        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT source, unique_code 
                            FROM api_product_data_source 
                            WHERE product_id = {0}
                            """.format(product_id))
            links = cursor.fetchall()
        
        unique_codes = [code[1] for code in links]
        if clean_url(url)[1] in unique_codes:
            print('user is already tracking this product\n Exit')
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        
        unique_codes.append(clean_url(url)[1])
        unique_codes = tuple(unique_codes)
        print(unique_codes)
        
        print('checking if product already exists...', end=' ')
        # check if product exists
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT product_id, count(unique_code) 
                            FROM api_product_data_source 
                            WHERE unique_code IN {0}
                            GROUP BY product_id
                            HAVING count(unique_code) = {1}
                            """.format(unique_codes, len(unique_codes)))
            row = cursor.fetchall() 
            
        prod_ids = [r[0] for r in row]  
        #print("potential product matches:", prod_ids)
        
        if len(prod_ids) == 1:
            prod_ids = tuple([prod_ids[0],prod_ids[0]]) 
        else:
            prod_ids = tuple(prod_ids) 
            
        # check if product exists
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT product_id, count(unique_code) 
                            FROM api_product_data_source 
                            WHERE product_id IN {0}
                            GROUP BY product_id
                            HAVING count(unique_code) = {1} 
                            """.format(prod_ids, len(unique_codes)))
            prods = cursor.fetchall() 
            
        # product exists
        if len(prods) > 0:
            print('product exists!!\n Product: %s' % prods[0][0])
            
            new_product_id = prods[0][0]
            
            # if User_Products.objects.filter(user=self.request.user, product=Product.objects.get(id=new_product_id)).exists():
            if User_Products.objects.filter(user=User.objects.get(pk=1), product=Product.objects.get(id=new_product_id)).exists():
                print('User Already tracking product\n Exit')
                return Response(status.HTTP_208_ALREADY_REPORTED)
            
            # delete product/ user connection to product
            ProductDelete.delete(self,request, product_id)
            
            #user_prod = User_Products(user=self.request.user, product=Product.objects.get(id=product_id))
            user_prod = User_Products(user=User.objects.get(pk=2), product=Product.objects.get(id=new_product_id))
            user_prod.save()
            
            serializer = ProductSumSerializer_HOME(Product_Summary.objects.filter(product=Product.objects.get(id=new_product_id)), many=True)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)  
        
        else:
            
            print('product does not exist\nchecking if link in database...')
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT unique_code
                        FROM api_product_data_source 
                        WHERE unique_code = %s
                        """, [clean_url(url)[1]])
                link_exists = cursor.fetchall() 
                
            if len(link_exists) == 0:
                print(' link not in database')
                product_meta  = CreateProduct.ddd(self, clean_url(url))
                
            
            else:
                print(' link in database') 
                with connection.cursor() as cursor:
                    cursor.execute("""
                                    SELECT DISTINCT name, brand, image
                                    FROM api_product_data_source ds
                                    INNER JOIN api_product p
                                    ON ds.product_id = p.id
                                    WHERE unique_code = %s
                                    """, [clean_url(url)[1]])
                    product_meta = cursor.fetchone()
                
            # create table instances
            print('adding data to database...')
            
            print(' created product instance')
            prod = Product(name=product_meta[0], brand=product_meta[1], image=product_meta[2])
            prod.save()

            print(' created user_product instance')
            #user_prod = User_Products(user=self.request.user, product=prod)
            user_prod = User_Products(user=User.objects.get(pk=2), product=prod)
            user_prod.save()
        
            for link in links:
                print(' created data_source instance for', link[1])
                link = Product_Data_Source(source=link[0], unique_code=link[1], product=prod)
                link.save()
            
            print(' created data_source instance for', clean_url(url)[1])
            link = Product_Data_Source(source=clean_url(url)[0], unique_code=clean_url(url)[1], product=prod)
            link.save()
            
            # delete product/ user connection to product
            print(' disconnecting user from old product')
            ProductDelete.delete(self,request, product_id)
        
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT review, sentiment_label, rating
                            FROM api_product_reviews
                            WHERE unique_code IN {0}
                                """.format(unique_codes))
                rows = cursor.fetchall() 
            
            print(' creating summary instance')
            serializer = CreateProduct.www(self,prod, rows)
            
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
    
        
class GetSentimentNewReviews(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        review = request.POST.getlist('review')
    
        return Response(analyseMultiple(review))        

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
    
    permission_classes  = [IsAuthenticated]
    
    def get(self, request, product_id):
        
        print(product_id)
        
        with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT DISTINCT unique_code
                            FROM api_product_data_source
                            WHERE product_id = %s
                            """, [product_id])
                unique_codes = cursor.fetchall() 
        
        unique_codes = [uni_code[0] for uni_code in unique_codes]
        
    
        serializer = SentimentDataSerializer_Dash(Product_Reviews.objects.filter(unique_code__in=unique_codes), many=True)
            
        datalist = pd.DataFrame(serializer.data)
        datalist['date'] = pd.to_datetime(datalist['date'], yearfirst=True)
        datalist['month'] = datalist['date'].dt.month
        last_year = datetime.now() - timedelta(days=365)
        filtered_datalist = datalist.loc[datalist['date'] > last_year]
        agg_datalist = filtered_datalist.groupby(['month','sentiment_label'])['sentiment_label'].count().reset_index(name='sentiment_count')
        chart_data = [[0]*12 for num in range(3)]

        for _, row in agg_datalist.iterrows():
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

    def get(self, request):
        url = request.GET.get('url')
        date = request.GET.get('date')
        return Response(scrape_reviews(url,date))
    
    
class GetCateogoryData(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, product_id):
        
        serializer = Product_Categories_Dash(Product_Data_Source.objects.filter(product_id=product_id), many=True)
        
        return Response(serializer.data)
        
  
#_____________________________________________________________________________________________________________________________
# DELETE Requests  

class ProductDelete(APIView):
    
    permission_classes  = [IsAuthenticated]
    
    def delete(self, request, product_id):

        # Delete for user table, not whole product
        User_Products.objects.filter(user=self.request.user,product=product_id).delete()
        #User_Products.objects.filter(user=User.objects.get(id=2),product=product_id).delete()
        
        # Delete product if no user is tracking (no point storing irrelevant data)
        if User_Products.objects.filter(product=product_id).exists() == False:
            
            
            with connection.cursor() as cursor:
                cursor.execute("""
                            SELECT DISTINCT unique_code, source
                            FROM api_product_data_source 
                            WHERE product_id = %s
                            """, [product_id])
                links = cursor.fetchall()
                
            Product.objects.filter(pk=product_id).delete()
                
            for link in links:
                print(link)
                if Product_Data_Source.objects.filter(unique_code=link[0]).exists() == False:
                    Product_Reviews.objects.filter(unique_code=link[0]).delete()
                    Source_date.objects.filter(source=link[1]).delete()
            

        return Response(status=status.HTTP_204_NO_CONTENT)
     
