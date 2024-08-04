from django.urls import path
from . import views

urlpatterns = [
    
    # change this for user specific
    path("product/", views.CreateProductView.as_view(), name='product-list'),
    
    
    path("user/products/", views.ListUserProduct.as_view(), name="show-user-prods"),
    path("product/<int:pk>/", views.GetProds.as_view(), name='user-remove-product'),
    path("try/<int:product_id>/", views.GetUProds.as_view(), name='user-remove-product'),
    #path("user/product/<int:product_id>/", views.GetProductDetails.as_view(), name='user-remove-product'),
    
    
    # Valid Urls (use in Project)
    path("user/product/home", views.GetUserProduct_HomePage.as_view(), name='user-product-home'),
    path("user/product/dashboard/sentiment/<int:product_id>/", views.GetReviewSent_Dash.as_view(), name='product-dashboard-sent'),
    path("user/product/dashboard/meta/<int:product_id>/", views.GetProduct_Meta_Dash.as_view(), name='product-dashboard-meta'),
    path("user/product/dashboard/summ/<int:product_id>/", views.GetProductSum_Dash.as_view(), name='product-dashboard-summ'),
    
]
