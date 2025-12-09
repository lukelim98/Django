from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.

# ========================================
# Author Model
# ========================================
class Author(models.Model):
    """
    Represents an author who can write blog posts.

    Each author has basic identity information and can be
    linked to multiple Post objects via a ForeignKey
    relationship (see Post model).
    """
    first_name = models.CharField(max_length=100)   # Author's first name
    last_name = models.CharField(max_length=100)    # Author's last name
    email = models.EmailField()                     # Author's email address

    def full_name(self):
        """
        REturns the author's full name as a single string.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """
        String representation shown in Django admin and shell
        """
        return self.full_name()


# ========================================
# Tag Model
# ========================================
class Tag(models.Model):
    """
    Represents a tag (category/label) for organizing posts.

    A single tag can be associated with many posts,
    and a post can have multiple tags (Many-to-Many).
    """
    caption = models.CharField(max_length=20)

    def __str__(self):
        """
        Human-readable representation of the tag. 
        """
        return f"{self.caption}"


# ========================================
# Post Model
# ========================================
class Post(models.Model):
    """
    Represent a blog post.

    Includes metadata (title, date, slug), content,
    an optional image, a single author, and multiple tags.
    """
    title = models.CharField(max_length=150)                           # Post title
    excerpt = models.CharField(max_length=200)                         # Short summary (preview text)
    image = models.ImageField(upload_to="posts", null=True)            # Optional post image
    date = models.DateField(auto_now=True)                             # Date last updated
    slug = models.SlugField(unique=True, db_index=True)                # URL-friendly unique identifier
    content = models.TextField(validators=[MinLengthValidator(10)])    # Main post content (min 10 chars)
    author = models.ForeignKey(
        Author,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts"
    )                                                                  # Each post has one author
    tags = models.ManyToManyField(
        Tag 
    )                                                                  # Post can have multiple tags

    def __str__(self):
        return self.title

# ========================================
# Comment Model
# ========================================
class Comment(models.Model):
    """
    Represents a user comment on a blog post.

    Each comment belongs to exactly one Post.
    """
    user_name = models.CharField(
        max_length=120
    )                                           # Comment author's name
    user_email = models.EmailField()            # Comment author's email
    text = models.TextField(
        max_length=400
    )                                           # Comment content
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )                                           # Comment is tied to one post