from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()

class UserTests(TestCase):
    """
    Test suite for the custom user model.
    """
    def setUp(self):
        """
        Test suite setup.
        """
        self.user= User.objects.create_user(
            email='mikailsimsek@mail.com',
            first_name='Mikail',
            last_name='Simsek',
            password='qwerty123',
        )

    def test_str(self):
        """
        Test string representation.
        """
        self.assertEqual(str(self.user), 'Mikail Simsek')

    def test_get_full_name_method(self):
        """
        Test get full name method.
        """
        self.assertEqual(self.user.get_full_name(), 'Mikail Simsek')