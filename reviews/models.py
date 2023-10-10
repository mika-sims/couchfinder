from django.db import models
from django.contrib.auth import get_user_model
from profiles.models import Profile

from .managers import ReviewManager


class Review(models.Model):
    """
    Model for storing user reviews
    """

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reviews"
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="reviews", default=1
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(get_user_model(), related_name="review_likes")

    objects = ReviewManager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Review by {self.user.get_full_name()}"

    def number_of_likes(self):
        """
        Return the number of likes for the review
        """
        return self.likes.count()
