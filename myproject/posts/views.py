from django.shortcuts import render
from .models import Post
from django.http import HttpResponse

# Create your views here.
def post_lists(request):
    posts = Post.objects.all().order_by('date')
    return render(request, 'posts/posts_lists.html', { 'posts': posts})

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', { 'post': post})


def post_new(request):
    return render(request, 'posts/post_new.html')