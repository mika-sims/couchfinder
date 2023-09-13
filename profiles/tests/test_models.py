from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cities_light.models import Country, Region, City


from profiles.views import Profile


class ProfileTests(TestCase):
    """
    Test suite for the custom user model.
    """

    def setUp(self):
        """
        Test suite setup.
        """
        self.user = get_user_model().objects.create_user(
            first_name='Mikail',
            last_name='Simsek',
            email='mikailsimsek@mail.com',
            password='qwerty123.'
        )

        # Check if a profile already exists for the user
        self.profile = Profile.objects.filter(user=self.user).first()

    def test_profile_str_method(self):
        self.assertEqual(str(self.profile),
                         f'{self.user.first_name} {self.user.last_name}')
