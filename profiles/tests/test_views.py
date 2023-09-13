from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from cities_light.models import Country, Region, City

from profiles.models import Profile


class ProfileDetailViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create(
            first_name='Mikail',
            last_name='Simsek',
            email='mikailsimsek@mail.com',
            password='qwerty123'
        )
        
        self.profile = Profile.objects.filter(user=self.user).first()
        
        self.url = reverse('profiles:user-profile', kwargs={'pk': self.user.pk})

    def test_redirected_to_the_login_page(self):
        # When an unauthenticated user tries to access the profile details page,
        # they should be redirected to the login page
        response = self.client.get(self.url)
        
        self.assertRedirects(response, '/accounts/login/?next=' + self.url)

    def test_returns_200_for_authenticated_user(self):
        # When an authenticated user tries to access the profile details page,
        # they should be able to access it
        self.client.force_login(user=self.user)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)

    def test_get_current_user_pk(self):
        # When an authenticated user tries to access the profile details page,
        # the user's pk should be passed to the view
        self.client.force_login(user=self.user)
        
        response = self.client.get(self.url)
        profile = response.context['profile']
        self.assertEqual(profile.user.pk, self.user.pk)

    def test_get_another_user_pk(self):
        # When an authenticated user tries to access another user's profile details page,
        # the other user's pk should be passed to the view
        another_user = get_user_model().objects.create(
            first_name='Another',
            last_name='User',
            email='anotheruser@mail.com',
            password='qwerty123'
        )
        
        url = reverse('profiles:user-profile', kwargs={'pk': another_user.pk})
        
        self.client.force_login(user=self.user)
        
        response = self.client.get(url)
        profile = response.context['profile']
        self.assertEqual(profile.user.pk, another_user.pk)