from django.urls import path

from . import views

urlpatterns = [
    path("", views.ReviewView.as_view()),
    path("thank-you", views.ThankYouView.as_view()),
    path("all-reviews", views.ReviewsView.as_view()),
    path("all-reviews/favorite", views.AddFavoriteView.as_view()),
    path("all-reviews/<int:pk>", views.SingleReviewView.as_view(), name="single-review")
]