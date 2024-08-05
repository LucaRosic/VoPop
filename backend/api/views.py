from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ProductSerializer, UserProductSerializer, ProductSumSerializer_HOME, SentimentDataSerializer_Dash, ProductSumSerializer_Dash, ProductSerializer_Dash
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, User_Products, Product_Summary, Product_Reviews
from scrape.scrapper import scrape_reviews

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
    
    #def get_queryset(self):
        #user = self.request.user
        #return User_Products.objects.filter(user=user).select_related('Product')
    
    def perform_create(self, serializer):
        
        if serializer.is_valid():
            # Perfrom scraping and elt here
            # add to db 
            
            # add relevant attributes
            ##if Product.objects.filter(url=serializer.validated_data['url']).exists():
                # add to user product table
            ##else:
                ##data = scraper(serializer.validated_data['url'])
                ##cleaned_data = transform_data(data)
                # 
            print(scrape_reviews(serializer.validated_data['url']))
            
            #serializer.save(name='prod', category='prod cat', description='prod descript', image='prod img')
            print(serializer.data)
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
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        
        product_ids = User_Products.objects.filter(user=self.request.user).values_list('product', flat=True)
        
        print(Product_Summary.objects.all().values())
        
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
    

    
   
        
                               
        
        