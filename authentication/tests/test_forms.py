from django.forms import ValidationError
from django.http import HttpRequest
from django.test import TestCase
from django.contrib.auth import get_user_model

from authentication.forms import CustomSignupForm


class CustomSignupFormTest(TestCase):
    """
    Test suite for the custom signup form.
    """
    def setUp(self):
        """
        Test suite setup.
        """
        self.user = get_user_model().objects.create_user(
            first_name='Mikail',
            last_name='Simsek',
            email='mikailsimsek@mail.com',
            password='qwerty123',
        )

    def test_clean_email(self):
        """
        Test email validation. 
        Form should raise ValidationError if email is already in use.
        """
        form = CustomSignupForm(data={
            'first_name': 'Mikail',
            'last_name': 'Simsek',
            'email': self.user.email,
            'password1': 'qwerty123',
            'password2': 'qwerty123',
            'remember_me': True
        })
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        
    def test_save(self):
        """
        Test save method.
        """
        request = HttpRequest()
        request.session = {}
        form = CustomSignupForm(data={
            'first_name': 'Mikail',
            'last_name': 'Simsek',
            'email': 'testmail@mail.com',
            'password1': 'nottocommonpassword',
            'password2': 'nottocommonpassword',
            'remember_me': True
        })
        self.assertTrue(form.is_valid())
        user = form.save(request)
        self.assertEqual(user.email, 'testmail@mail.com')
        self.assertEqual(user.first_name, 'Mikail')
        self.assertEqual(user.last_name, 'Simsek')
        