from django.test import TestCase
from django.contrib.auth import get_user_model

from profiles.models import Profile
from profiles.signals import save_profile


class SignalsTest(TestCase):
    # Test suite for the signals.
    def setUp(self):
        self.User = get_user_model().objects.create_user(
            first_name='Mikail',
            last_name='Simsek',
            email='mikailsimsek@mail.com',
            password='qwerty123'
        )
        
        # Check if the profile already exists for the user
        self.profile = Profile.objects.filter(user=self.User).first()

    def test_create_profile_signal(self):
        # Test the create profile signal.
        self.assertEqual(self.profile.user, self.User)

    def test_save_profile_signal(self):
        # Test the save profile signal.
        save_profile(sender=self.User, instance=self.profile)
        # Check if the profile is saved
        self.assertTrue(self.profile)