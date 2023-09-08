from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    """
    Custom signup form to add first and last name fields.
    """
    first_name = forms.CharField(max_length=30, label='First Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    remember_me = forms.BooleanField(required=False, label='Remember Me',
                                     widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))

    def clean_email(self):
        """
        Validate email address.
        """
        email = self.cleaned_data['email']
        User = get_user_model()

        # Check if email is already in use by another user
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is being used by another user.")

        return email

    def save(self, request):
        """
        Save the user to the database.
        """
        user = super(CustomSignupForm, self).save(request)
        user.save()
        return user