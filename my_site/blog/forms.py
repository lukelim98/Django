from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """
    ModelForm for creating and validating Comment objects.

    This form is automatically generated frmo the Comment model.
    All model fields are included EXCEPT the `post` field, which
    is expected to be assigned programmatically in the view
    (e.g., when attaching the comment to a specific blog post).
    """
    class Meta:
        model = Comment

        # Exclude the `post` ForeignKey field since it will be set in the view
        exclude = ["post"]
        # fields = ["user_name", "user_email", "text"]

        # Customize human-readable labels for form fields
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "Comment": "text"
        }
        