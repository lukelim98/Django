from django.urls import path
from . import views

# ==========================
# URL Configuration for Blog App
# ==========================
# This module deinfes all URL routes for the blog application.
# Each path maps a URL pattern to a class-based view
urlpatterns = [
    
    # Starting page (homepage)
    # Example URL: /
    # Displays the lates or featured blog posts
    path(
        "",
        views.StartingPageView.as_view(),
        name='starting-page'
    ),

    # Post list page
    # Example URL: /posts
    # Displays a list of all blog posts
    path(
        "posts",
        views.PostsView.as_view(),
        name='posts-page'
    ),

    # Single post detail page
    # Example URL: /post/my-first-blog-post
    # Uses a slug to uniquely identify and load a post
    path(
        "post/<slug:slug>",
        views.PostDetailView.as_view(),
        name='post-detail-page'
    ),

    # Read Later feature (session-based storage)
    # Example URL: /read-later
    # Handles POST requests to save or remove posts from the user's
    # "Read Later" list, which is stored in the session
    path(
        "read-later",
        views.ReadLaterView.as_view(),
        name="read-later"
    )
]
