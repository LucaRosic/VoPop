from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # homepage
    path('', views.post_lists, name='list'),
    path('new-post/', views.post_new, name='page'),
    path('<slug:slug>', views.post_page, name='page'),
       
]