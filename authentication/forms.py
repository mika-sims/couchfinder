from django import forms
from django.contrib.auth import get_user_model
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