from django.urls import path
from . import views

urlpatterns = [
    
    # change this for user specific
    path("product/", views.CreateProductView.as_view(), name='product-list'),
    
    
    path("user/products/", views.ListUserProduct.as_view(), name="show-user-prods"),
    path("user/product/delete/<int:pk>/", views.DeleteUserProduct.as_view(), name='user-remove-product'),
]
