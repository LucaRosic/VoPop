from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField("Name", max_length=240)
    category = models.CharField("Category", max_length=240)
    url = models.CharField("URL", max_length=240)
    description = models.CharField("Description", max_length=240)
    image = models.CharField("Image", max_length=240)
    
    def __str__(self):
        return self.name
    
    
class User_Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
class Product_Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.CharField(max_length=8000)
    sentiment = models.DecimalField(max_digits=3, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=0)
    date = models.DateField()
 
    
class Product_Summary(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    summary = models.CharField(max_length=8000)
    avg_sentiment = models.DecimalField(max_digits=3, decimal_places=2)
    avg_rating = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    