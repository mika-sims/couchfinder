from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a user profile for every new account created.
    """
    if created:
        Profile.objects.create(user=instance)


def save_profile(sender, instance, **kwargs):
    """
    Save the user profile.
    """
    instance.save()