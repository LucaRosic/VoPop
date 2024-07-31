from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, User_Products

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "category", "url", "description", "image"]
        extra_kwargs = {"name": {"read_only": True}, \
            "category": {"read_only": True}, "description": {"read_only": True}, \
                "image": {"read_only": True}}
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}
        
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    
class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Products
        fields = ["id", "user", "product"]
        extra_kwargs = {"user": {"read_only": True},"product": {"read_only": True} }