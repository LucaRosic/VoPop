from django.contrib import admin
from .models import Product, User_Products, Product_Summary, Product_Reviews, Product_Data_Source

# Register your models here.
admin.site.register(Product)
admin.site.register(User_Products)
admin.site.register(Product_Summary)
admin.site.register(Product_Reviews)
admin.site.register(Product_Data_Source)