from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from cities_light.models import City, Region, Country
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    """
    Model for storing user profile information
    """

    COUCH_FINDER_STATUS_CHOICES = (
        ("hosting", "Hosting"),
        ("travelling", "Travelling"),
        ("busy", "Busy"),
    )

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True)
    image = CloudinaryField("image")
    bio = models.TextField(blank=True, default="")
    occupation = models.CharField(max_length=250, blank=True, default="")
    couch_status = models.CharField(
        max_length=20, choices=COUCH_FINDER_STATUS_CHOICES, default="busy"
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    class Meta:
        # Order by the user's first name
        ordering = ["user__first_name"]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def get_location(self):
        """
        Return the user's location
        """
        location = [self.city, self.region, self.country]

        # Filter out None values
        location = [item for item in location if item is not None]

        # Join the location values into a string
        location = ", ".join([item.name for item in location])

        return location
