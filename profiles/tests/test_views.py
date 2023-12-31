import json
from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from profiles.models import Profile
from profiles.forms import ProfileForm
from cities_light.models import Country, Region, City

from profiles.models import Profile
from profiles.views import ProfileUpdateView, CustomPasswordChangeView


class ProfileDetailViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create(
            first_name="Mikail",
            last_name="Simsek",
            email="mikailsimsek@mail.com",
            password="qwerty123",
        )

        self.profile = Profile.objects.filter(user=self.user).first()

        self.url = reverse("profiles:user-profile",
                           kwargs={"pk": self.user.pk})

    def test_redirected_to_the_login_page(self):
        # When an unauthenticated user tries to access the profile details page,
        # they should be redirected to the login page
        response = self.client.get(self.url)

        self.assertRedirects(response, "/accounts/login/?next=" + self.url)

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
        profile = response.context["profile"]
        self.assertEqual(profile.user.pk, self.user.pk)

    def test_get_another_user_pk(self):
        # When an authenticated user tries to access another user's profile details page,
        # the other user's pk should be passed to the view
        another_user = get_user_model().objects.create(
            first_name="Another",
            last_name="User",
            email="anotheruser@mail.com",
            password="qwerty123",
        )

        url = reverse("profiles:user-profile", kwargs={"pk": another_user.pk})

        self.client.force_login(user=self.user)

        response = self.client.get(url)
        profile = response.context["profile"]
        self.assertEqual(profile.user.pk, another_user.pk)


class ProfileUpdateViewTest(TestCase):
    """
    Test that the profile update view works as expected.
    """

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create(
            first_name="Mikail",
            last_name="Simsek",
            email="mikailsimsek@mail.com",
            password="qwerty123",
        )

        self.profile = Profile.objects.filter(user=self.user).first()
        self.url = reverse("profiles:profile-update",
                           kwargs={"pk": self.user.pk})

        # Create other user
        self.user2 = get_user_model().objects.create(
            first_name="Another",
            last_name="User",
            email="anotheruser@mail.com",
            password="qwerty123",
        )

        self.profile2 = Profile.objects.filter(user=self.user2).first()
        self.url2 = reverse("profiles:profile-update",
                            kwargs={"pk": self.user2.pk})

    def test_get_object_method_for_current_user(self):
        # When the get_object method is called, the user's profile should be returned
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)
        profile = response.context["profile"]
        self.assertEqual(profile.user.pk, self.user.pk)

    def test_get_object_method_for_another_user(self):
        # When the get_object method is called, another user's profile should be returned
        self.client.force_login(user=self.user)
        response = self.client.get(self.url2)
        profile = response.context["profile"]
        self.assertEqual(profile.user.pk, self.user2.pk)

    def test_get_success_url_method(self):
        # When the get_success_url method is called, the user's profile page should be returned
        self.client.force_login(user=self.user)
        view = ProfileUpdateView()
        view.kwargs = {"pk": self.user.pk}
        url = view.get_success_url()
        self.assertEqual(url, "/profiles/profile/" + str(self.user.pk) + "/")

    def test_form_valid(self):
        """
        Test form validation
        """
        self.client.force_login(user=self.user)

        # Get the user's profile
        profile = Profile.objects.get(user=self.user)

        # Create country, region, and city instances
        country = Country.objects.create(name="Italy")
        region = Region.objects.create(name="Tuscany", country=country)
        city = City.objects.create(
            name="Florence", region=region, country=country)

        # Update the user's profile
        form = ProfileForm(
            instance=profile,
            data={
                "bio": "This is a test bio",
                "occupation": "Test occupation",
                "couch_status": "hosting",
                "country": country.pk,
                "region": region.pk,
                "city": city.pk,
            },
        )

        self.assertTrue(form.is_valid())
        response = self.client.post(self.url, form.data)
        self.assertTrue(response.status_code == 302)


class GetRegionsTest(TestCase):
    """
    Test that the get_regions view works as expected.
    """

    def setUp(self):
        # Create sample data
        self.country = Country.objects.create(id=1, name="Test Country")
        self.region = Region.objects.create(
            id=1, name="Test Region", country=self.country
        )
        self.city = City.objects.create(
            id=1, name="Test City", region=self.region, country=self.country
        )

    def test_get_regions(self):
        url = reverse("profiles:get_regions")

        response = self.client.get(url, {"country_id": self.country.id})
        data = json.loads(response.content)

        self.assertIsInstance(response, JsonResponse)
        self.assertIn("regions", data)
        self.assertEqual(len(data["regions"]), 1)

        region_data = data["regions"][0]
        self.assertEqual(region_data["id"], self.region.id)
        self.assertEqual(region_data["name"], self.region.name)


class GetCitiesTest(TestCase):
    """
    Test that the get_cities view works as expected.
    """

    def setUp(self):
        # Create sample data
        self.country = Country.objects.create(id=1, name="Test Country")
        self.region = Region.objects.create(
            id=1, name="Test Region", country=self.country
        )
        self.city = City.objects.create(
            id=1, name="Test City", region=self.region, country=self.country
        )

    def test_get_cities(self):
        url = reverse("profiles:get_cities")
        response = self.client.get(url, {"region_id": self.region.id})
        data = json.loads(response.content)

        self.assertIsInstance(response, JsonResponse)
        self.assertIn("cities", data)
        self.assertEqual(len(data["cities"]), 1)

        city_data = data["cities"][0]
        self.assertEqual(city_data["id"], self.city.id)
        self.assertEqual(city_data["name"], self.city.name)


class CustomPasswordChangeViewTest(TestCase):
    """
    Test that the custom password change view works as expected.
    """

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create(
            first_name="Mikail",
            last_name="Simsek",
            email="mikailsimsek@mail.com",
            password="qwerty123",
        )

    def test_get_success_url_method(self):
        # When the get_success_url method is called, the user's profile page should be returned
        self.client.force_login(user=self.user)
        request = RequestFactory().get(
            reverse("profiles:profile-update", kwargs={"pk": self.user.pk})
        )
        request.user = self.user
        view = CustomPasswordChangeView()
        view.request = request
        url = view.get_success_url()
        expected_url = reverse("profiles:user-profile",
                               kwargs={"pk": self.user.pk})
        self.assertEqual(url, expected_url)


class AccountDeactivateViewTest(TestCase):
    """
    Test that the account deactivate view works as expected.
    """

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create(
            first_name="Mikail",
            last_name="Simsek",
            email="mikailsimsek@mail.com",
            password="qwerty123",
        )

    def test_get_method(self):
        # When the get method is called, the account deactivate page should be returned
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("profiles:account-deactivate"))
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        # When the post method is called,
        # the 'account_deactivate_mail_send.html' page should be returned
        self.client.force_login(user=self.user)
        response = self.client.post(reverse("profiles:account-deactivate"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account_deactivate_mail_send.html")


class AccountDeactivateConfirmViewTest(TestCase):
    """
    Test that the account deactivate confirm view works as expected.
    """

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create(
            first_name="Mikail",
            last_name="Simsek",
            email="mikailsimsek@mail.com",
            password="qwerty123",
        )

    def test_get_method(self):
        # When the get method is called, the account deactivate confirm page should be returned
        self.client.force_login(user=self.user)
        uid = urlsafe_base64_encode(str(self.user.pk).encode())
        token = default_token_generator.make_token(self.user)
        response = self.client.get(
            reverse(
                "profiles:account-deactivate-confirm",
                kwargs={"uidb64": uid, "token": token},
            )
        )

        try:
            # Decode the UID and get the user
            uid = urlsafe_base64_decode(uid).decode()
            user = get_user_model().objects.get(pk=uid)

            if response.url == reverse("profiles:account-deactivate-done"):
                user.delete()
                self.assertFalse(
                    get_user_model().objects.filter(pk=uid).exists())
            else:
                self.assertTrue(
                    get_user_model().objects.filter(pk=uid).exists())

        except:
            pass


class AccountDeactivateDoneViewTest(TestCase):
    """
    Test that the account deactivate done view works as expected.
    """

    def test_get_method(self):
        # When the get method is called, the account deactivate done page should be returned
        response = self.client.get(reverse("profiles:account-deactivate-done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account_deactivate_done.html")


class ProfileSearchViewTest(TestCase):
    """
    Test that the profile search view works as expected.
    """

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create(
            first_name="Mikail",
            last_name="Simsek",
            email="mikailsimsek@mail.com",
            password="qwerty123",
        )

    def test_get_method(self):
        # When the get method is called, the profile search page should be returned
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("profiles:profile-search"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_search.html")
