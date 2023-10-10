from django.db import models


class ReviewManager(models.Manager):
    def get_reviews_for_user(self, user):
        return self.filter(user=user)

    def get_reviews_for_profile(self, profile):
        return self.filter(profile=profile)
