from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTests(TestCase):
    """
    Test suite for the custom user model manager.
    """
    def setUp(self):
        """
        Test suite setup.
        """
        self.User = get_user_model()
        self.manager = self.User.objects
        self.email = 'mikailsimsek@mail.com'
        self.first_name = 'Mikail'
        self.last_name = 'Simsek'
        self.password = 'qwerty123'

    def test_create_user(self):
        """
        Test creating a user.
        """
        user = self.manager.create_user(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
        )

        with self.assertRaises(ValueError):
            self.manager.create_user(
                email='',
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
            )
        with self.assertRaises(ValueError):
            self.manager.create_user(
                email=self.email,
                first_name='',
                last_name=self.last_name,
                password=self.password,
            )
        with self.assertRaises(ValueError):
            self.manager.create_user(
                email=self.email,
                first_name=self.first_name,
                last_name='',
                password=self.password,
            )

    def test_create_superuser(self):
        """
        Test creating a superuser.
        """
        user = self.manager.create_superuser(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
        )

        with self.assertRaises(ValueError):
            self.manager.create_superuser(
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                is_staff=False,
            )
        with self.assertRaises(ValueError):
            self.manager.create_superuser(
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                is_superuser=False,
            )
        with self.assertRaises(ValueError):
            self.manager.create_superuser(
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                is_admin=False,
            )
        with self.assertRaises(ValueError):
            self.manager.create_superuser(
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                is_active=False,
            )