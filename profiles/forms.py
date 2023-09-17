from django import forms

from profiles.models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form for updating the user profile details.
    """

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
