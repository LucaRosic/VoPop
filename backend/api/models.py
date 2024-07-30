from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField("Name", max_length=240)
    category = models.CharField("Category", max_length=240)
    url = models.CharField("URL", max_length=240)
    description = models.CharField("Description", max_length=240)
    image = models.CharField("Image", max_length=240)
    
    def __str__(self):
        return self.name