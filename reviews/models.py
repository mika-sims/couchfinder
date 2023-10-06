from django.db import models
from django.contrib.auth import get_user_model


class Review(models.Model):
    """
    Model for storing user reviews
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(get_user_model(), related_name='review_likes')
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Review by {self.user.get_full_name()}'
    
    def number_of_likes(self):
        """
        Return the number of likes for the review
        """
        return self.likes.count()