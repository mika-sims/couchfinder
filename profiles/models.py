from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from cities_light.models import Country, Region, City
from django.urls import reverse


class Profile(models.Model):
    """
    Model for storing user profile information
    """
    COUCH_FINDER_STATUS_CHOICES = (
        ('hosting', 'Hosting'),
        ('travelling', 'Travelling'),
        ('busy', 'Busy'),
    )

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = CloudinaryField('image')
    bio = models.TextField(blank=True, default='')
    occupation = models.CharField(max_length=250, blank=True, default='')
    couch_status = models.CharField(
        max_length=20, choices=COUCH_FINDER_STATUS_CHOICES, default='busy')
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
