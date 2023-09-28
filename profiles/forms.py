from django import forms
from cities_light.models import City, Region, Country
from profiles.models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form for updating the user profile details.
    """

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=False)
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(), required=False)
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), required=False)

    class Meta:
        """
        Meta class for ProfileForm.
        """
        model = Profile
        fields = (
            'image',
            'bio',
            'occupation',
            'couch_status',
            'country',
            'region',
            'city',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders
        self.fields['bio'].widget.attrs['placeholder'] = 'Tell us about yourself'
        self.fields['occupation'].widget.attrs['placeholder'] = 'Your occupation'
        self.fields['image'].required = False
