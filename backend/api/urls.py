from django.urls import path
from . import views

urlpatterns = [
    
    # change this for user specific
    path("product/", views.CreateProduct.as_view(), name='product-list'),
    
    # Valid Urls (use in Project)
    path("user/product/home/", views.GetUserProduct_HomePage.as_view(), name='user-product-home'),
    path("user/product/dashboard/sentiment/<int:product_id>/", views.GetReviewSent_Dash.as_view(), name='product-dashboard-sent'),
    path("user/product/dashboard/meta/<int:product_id>/", views.GetProductMeta_Dash.as_view(), name='product-dashboard-meta'),
    path("user/product/dashboard/summ/<int:product_id>/", views.GetProductSum_Dash.as_view(), name='product-dashboard-summ'),
    
]
