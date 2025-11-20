from datetime import date

from django.shortcuts import render
from .models import Post


# Create your views here.


def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, 'blog/index.html', {
        "posts": latest_posts
    })


def posts(request):
    sorted_posts = Post.objects.all().order_by("-date")
    return render(request,
                'blog/all-posts.html',
                {
                    "posts":sorted_posts
                })


def post_detail(request, slug):
    selected_post = Post.objects.get(slug=slug)
    return render(request, "blog/post-detail.html",{
        "post":selected_post
    })
