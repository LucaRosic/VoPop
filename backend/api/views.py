from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, ProductSerializer, UserProductSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, User_Products

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
        #return Product.objects.filter()
    
    def perform_create(self, serializer):
        
        if serializer.is_valid():
            # Perfrom scraping and elt here
            # add to db 
            
            # add relevant attributes
            serializer.save(name='prod', category='prod cat', description='prod descript', image='prod img')
        else:
            print(serializer.errors)

class ListUserProduct(generics.ListCreateAPIView):
    
    serializer_class = UserProductSerializer
    
    permission_classes = [AllowAny]
    
    queryset = User_Products.objects.all()

class DeleteUserProduct(generics.DestroyAPIView):
    
    queryset = User_Products.objects.all()
    
    permission_classes = [AllowAny]
    
    #def get_queryset(self):
        #user = self.request.user
        #return User_Products.objects.filter(user=user)      