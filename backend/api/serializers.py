from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, User_Products, Product_Summary, Product_Reviews

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "category", "url", "brand", "image"]
        extra_kwargs = {"name": {"read_only": True}, \
            "category": {"read_only": True}, "brand": {"read_only": True}, \
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
<<<<<<< HEAD
        fields = ['product', 'summary', 'avg_sentiment', 'date']
        extra_kwargs = {"product": {"read_only": True}, "summary": {"read_only": True}, \
            "avg_sentiment": {"read_only": True}, "date": {"read_only": True}}
=======
        fields = ['product', 'overview', 'avg_sentiment', 'review_count', 'postive_count', 'negative_count', 'date']
        extra_kwargs = {"product": {"read_only": True}, "overview": {"read_only": True}, \
            "avg_sentiment": {"read_only": True}, "review_count": {"read_only": True}, \
                "postive_count": {"read_only": True}, "negative_count": {"read_only": True}, "date": {"read_only": True}}
>>>>>>> Dev
        

#______________________________________________________________________________________________________
# DASHBOARD PAGE SERIALIZERS

class SentimentDataSerializer_Dash(serializers.ModelSerializer):
    
    class Meta:
        model = Product_Reviews
<<<<<<< HEAD
        fields = ['sentiment', 'sentiment_label', 'date']
        extra_kwargs = {"sentiment": {"read_only": True}, "sentiment_label": {"read_only": True}, "date": {"read_only": True}}
=======
        fields = ['sentiment_label', 'date']
        extra_kwargs = {"sentiment_label": {"read_only": True}, "date": {"read_only": True}}
>>>>>>> Dev
  
        
class ProductSerializer_Dash(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "image", 'brand']
        extra_kwargs = {"name": {"read_only": True}, "image": {"read_only": True}, "brand": {"read_only": True}}

class ProductSumSerializer_Dash(serializers.ModelSerializer):
    
    class Meta:
        model = Product_Summary
        fields = ['product', 'summary', 'avg_sentiment', 'avg_rating', 'date']
        extra_kwargs = {"product": {"read_only": True}, "summary": {"read_only": True}, \
            "avg_sentiment": {"read_only": True}, "avg_rating": {"read_only": True}, "date": {"read_only": True}, }

        