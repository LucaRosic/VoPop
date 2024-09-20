from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(User_Products)
admin.site.register(Product_Summary)
admin.site.register(Product_Reviews)
admin.site.register(Product_Data_Source)
admin.site.register(Source_date)