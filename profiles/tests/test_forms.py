from django.test import TestCase
from profiles.models import Profile
from profiles.forms import ProfileForm


class ProfileFormTests(TestCase):
    """
    Tests for ProfileForm.
    """

    def test_init_method(self):
        """
        Test the __init__() method of ProfileForm.
        """
        form = ProfileForm()
        self.assertEqual(form.Meta.model, Profile)
        self.assertEqual(
            form.Meta.fields,
            (
                "image",
                "bio",
                "occupation",
                "couch_status",
                "country",
                "region",
                "city",
            ),
        )
        self.assertEqual(
            form.fields["bio"].widget.attrs["placeholder"], "Tell us about yourself"
        )
        self.assertEqual(
            form.fields["occupation"].widget.attrs["placeholder"], "Your occupation"
        )
