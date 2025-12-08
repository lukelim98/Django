from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from .forms import CommentForm


# Create your views here.


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, 'blog/index.html', {
#         "posts": latest_posts
#     })

class StartingPageView(TemplateView):
    template_name = "blog/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Post.objects.all().order_by("date")[:3]
        context['posts'] = latest_posts
        return context



# def posts(request):
#     sorted_posts = Post.objects.all().order_by("-date")
#     return render(request,
#                 'blog/all-posts.html',
#                 {
#                     "posts":sorted_posts
#                 })

class PostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]


# def post_detail(request, slug):
#     selected_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html",{
#         "post":selected_post,
#         "post_tags": selected_post.tags.all()
#     })

class PostDetailView(DetailView):
    # Which template to render for this view
    template_name = "blog/post-detail.html"
    
    # Tell django which model this detail page is for
    model = Post

    # What name the template should use to access the object
    # Instead of using {{ object }}, you can use {{ post }}
    context_object_name = "post"

    # THe model field Django should use to look up the object
    # Here we want to find Post objects by their slug (not by ID)
    slug_field = "slug"

    # THe name of the URL parameter that contains the slug value
    # Example URL: /posts/<slug:slug>/
    # THe part "slug" becomes self.kwars["slug"]
    slug_url_kwarg = "slug"

    # Add extra data to the template context
    def get_context_data(self, **kwargs):
        # Get the default context from Django (this includes "post")
        context = super().get_context_data(**kwargs)

        # The Post object that DetailView has already retrieved
        post = self.object

        # Add the tags related to this post to the template context
        context["post_tags"] = post.tags.all()

        # Add CommentForm to the template context
        context['comment_form'] = CommentForm()

        return context

    
