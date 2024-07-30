from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product

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
    
    def perform_create(self, serializer):
        
        if serializer.is_valid():
            serializer.save(name='prod', category='prod cat', description='prod descript', image='prod img')
        else:
            print(serializer.errors)
        