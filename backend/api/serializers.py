from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, User_Products, Product_Summary, Product_Reviews

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "category", "url", "description", "image"]
        extra_kwargs = {"name": {"read_only": True}, \
            "category": {"read_only": True}, "description": {"read_only": True}, \
                "image": {"read_only": True}, "image": {"read_only": True}}
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}
        
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    
class UserProductSerializer(serializers.ModelSerializer):
    #product = ProductSerializer()
    #user = UserSerializer()
    
    class Meta:
        model = User_Products
        fields = ["id", "user", "product"]
        extra_kwargs = {"user": {"read_only": True},"product": {"read_only": True} }
        lookup_field = 'product_id'



#______________________________________________________________________________________________________
# HOME PAGE SERIALIZERS

class ProductSerializer_HOME(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "image"]
        extra_kwargs = {"name": {"read_only": True}, "image": {"read_only": True}}

        
class ProductSumSerializer_HOME(serializers.ModelSerializer):
    product = ProductSerializer_HOME()
    
    class Meta:
        model = Product_Summary
        fields = ['product', 'summary', 'avg_sentiment', 'date']
        extra_kwargs = {"product": {"read_only": True}, "summary": {"read_only": True}, \
            "avg_sentiment": {"read_only": True}, "date": {"read_only": True}}
        

#______________________________________________________________________________________________________
# DASHBOARD PAGE SERIALIZERS

class SentimentDataSerializer_Dash(serializers.ModelSerializer):
    
    class Meta:
        model = Product_Reviews
        fields = ['sentiment', 'date']
        extra_kwargs = {"sentiment": {"read_only": True}, "date": {"read_only": True}}
  
        
class ProductSerializer_Dash(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "image", 'description']
        extra_kwargs = {"name": {"read_only": True}, "image": {"read_only": True}, "description": {"read_only": True}}

class ProductSumSerializer_Dash(serializers.ModelSerializer):
    
    class Meta:
        model = Product_Summary
        fields = ['product', 'summary', 'avg_sentiment', 'avg_rating', 'date']
        extra_kwargs = {"product": {"read_only": True}, "summary": {"read_only": True}, \
            "avg_sentiment": {"read_only": True}, "avg_rating": {"read_only": True}, "date": {"read_only": True}, }

        
    
   