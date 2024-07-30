from django.urls import path
from . import views

urlpatterns = [
    path("product/", views.CreateProductView.as_view(), name='product-list')
]
