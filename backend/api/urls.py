from django.urls import path
from . import views

urlpatterns = [
    
    # Post Request
    path("product/", views.CreateProduct.as_view(), name='create-product'),
    
    # Get Requests
    path("product/home/", views.GetUserProduct_Home.as_view(), name='product-home'),
    path("product/dashboard/sentiment/<int:product_id>/", views.GetReviewSent_Dash.as_view(), name='product-dashboard-sent'),
    path("product/dashboard/meta/<int:product_id>/", views.GetProductMeta_Dash.as_view(), name='product-dashboard-meta'),
    path("product/dashboard/summ/<int:product_id>/", views.GetProductSum_Dash.as_view(), name='product-dashboard-summ'),
    
]
