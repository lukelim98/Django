from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator

# Create your models here.
class Review(models.Model):
    user_name = models.CharField(max_length=100)
    review_text = models.TextField(validators=[MaxLengthValidator(200)])
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user_name}, {self.review_text}, {self.rating}"