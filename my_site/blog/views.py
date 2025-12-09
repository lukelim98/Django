from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views import View
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, 'blog/index.html', {
#         "posts": latest_posts
#     })

# =======================================
# Starting Page View
# =======================================
class StartingPageView(TemplateView):
    """
    Renders the blog starting (home) page.

    Displays a limtied number of the most recent posts.
    This view uses TempalteView and manually injects
    post data into the template context.
    """
    template_name = "blog/index.html"
    
    def get_context_data(self, **kwargs):
        """
        Adds the latest blog posts to the template context.

        Returns:
            dict: Context dictionary containing the latest posts.
        """
        context = super().get_context_data(**kwargs)

        # Retrieve the 3 most recent posts ordered by date
        latest_posts = Post.objects.all().order_by("date")[:3]

        # Add posts to the context so they are accessible in the template
        context['posts'] = latest_posts

        return context



# def posts(request):
#     sorted_posts = Post.objects.all().order_by("-date")
#     return render(request,
#                 'blog/all-posts.html',
#                 {
#                     "posts":sorted_posts
#                 })


# =======================================
# Posts List View
# =======================================
class PostsView(ListView):
    """
    Displays a list of all blog posts.

    Uses Django's ListView to automatically:
    - Query the Post model
    - Pass objects as `object_list` to the template
    """

    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]  # Show newest posts first


# def post_detail(request, slug):
#     selected_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html",{
#         "post":selected_post,
#         "post_tags": selected_post.tags.all()
#     })

# class PostDetailView(DetailView):
#     # Which template to render for this view
#     template_name = "blog/post-detail.html"
    
#     # Tell django which model this detail page is for
#     model = Post

#     # What name the template should use to access the object
#     # Instead of using {{ object }}, you can use {{ post }}
#     context_object_name = "post"

#     # THe model field Django should use to look up the object
#     # Here we want to find Post objects by their slug (not by ID)
#     slug_field = "slug"

#     # THe name of the URL parameter that contains the slug value
#     # Example URL: /posts/<slug:slug>/
#     # THe part "slug" becomes self.kwars["slug"]
#     slug_url_kwarg = "slug"

#     # Add extra data to the template context
#     def get_context_data(self, **kwargs):
#         # Get the default context from Django (this includes "post")
#         context = super().get_context_data(**kwargs)

#         # The Post object that DetailView has already retrieved
#         post = self.object

#         # Add the tags related to this post to the template context
#         context["post_tags"] = post.tags.all()

#         # Add CommentForm to the template context
#         context['comment_form'] = CommentForm()

#         return context


# =======================================
# Post Detail & Comment View
# =======================================
class PostDetailView(View):
    """
    Handles displaying a single blog post and processing user comments.

    - Get request: Displays the post details and an empty comment form
    - POST request: Validates and saves a new comment for the post
    """

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        """
        Handles GET requests.

        Retrieves the post identified by the slug and renders
        the post detail page with associated tags and a comment form.
        """

        # Retrieve the post using the unique slug
        post = Post.objects.get(slug=slug)

        # Context data passed to the template
        context = {
            "post": post,                       # Post object
            "post_tags": post.tags.all(),       # Related tags
            "comment_form": CommentForm(),      # Empty comment form
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }

        # Render the post detail tempalte
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        """
        Handles POST requests.

        Processes the submitted comment form, attaches the comment
        to the corresponding post, and saves it to the database.
        """
        
        # Bind submitted form data to CommentForm
        comment_form = CommentForm(request.POST)

        # Retrieve the post being commented on
        post = Post.objects.get(slug=slug)
         
        if comment_form.is_valid():
            # Create Comment instance without saving it DB yet
            comment = comment_form.save(commit=False)

            # Associate the comment with the current post
            comment.post = post

            # Save the comment to the database
            comment.save()

            # Rdirect to the same post detail page
            # (Prevents form resubmission on page refresh)
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        # If the form is invalid, re-render the page with errors
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,            # Form with validation errors
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)
    


# =======================================
# Read Later View (Session-Based Feature)
# =======================================
# This view manages the "Read Later" functionality for the blog
#
# Key Behavior:
# - GET request: Displays all posts the user has saved for later
#   (stored inside the session, so no login required).
# - POST request: Adds a post ID to the user's session-based list.
#
# Notes:
# - Data is stored per user session, not in the database.
# - Ideal for casual users who read posts without creating accounts.
class ReadLaterView(View):
    def get(self, request):
        """
        Handles GET requests.

        Displays all posts that the user previously marked
        to "read later". If non exist, the template is informed.
        """

        # Retrieve saved post IDs from the session
        stored_posts = request.session.get("stored_posts")

        context = {}

        # If no saved posts, send an empty list and flag
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            # Fetch posts matching saved IDs
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        # REnder the page showing saved posts
        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        """
        Handles POST requests.

        Saves a selected post ID to the user's session so they can
        revisit it later. If the post is already stored, it is ignored.
        """
        
        # Retrieve existing list from session (or create a new one)
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []

        # Extract post ID from form submission
        post_id = int(request.POST["post_id"])
        
        # Add the post if it is not already saved
        if post_id not in stored_posts:
            stored_posts.append(post_id)

        else:
            stored_posts.remove(post_id)
        # Save updated list back to the session
        request.session["stored_posts"] = stored_posts

        # Redirect to the hompage after saving
        return HttpResponseRedirect("/")