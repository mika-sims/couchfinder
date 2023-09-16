from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import View, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordChangeView as AllauthPasswordChangeView

from .models import Profile
from . import forms


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying the user profile details.
    """
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Get the 'pk' parameter from the URL
        user_pk = self.kwargs.get('pk')

        if self.request.user.pk == user_pk:
            # If it's the user's own profile, return their own profile
            return self.request.user.profile
        else:
            # If it's another user's profile, return that user's profile
            user = get_user_model().objects.get(pk=user_pk)
            return user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating the user profile details.
    """
    model = Profile
    form_class = forms.ProfileForm
    template_name = 'profile_update.html'

    def get_object(self, queryset=None):
        # Get the 'pk' parameter from the URL
        user_pk = self.kwargs.get('pk')

        if self.request.user.pk == user_pk:
            # If it's the user's own profile, return their own profile
            return self.request.user.profile
        else:
            # If it's another user's profile, return that user's profile
            user = get_user_model().objects.get(pk=user_pk)
            return user.profile

    def get_success_url(self):
        # Get the 'pk' parameter from the URL
        user_pk = self.kwargs.get('pk')
        return reverse('profiles:user-profile', kwargs={'pk': user_pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context

    def form_valid(self, form):
        form.save()
        print("Profile updated successfully")
        return super(ProfileUpdateView, self).form_valid(form)


def upload_image(request):
    # Upload the image and return the URL using a JSON response
    if request.method == 'POST' and request.FILES['profile_picture']:
        profile = request.user.profile
        profile.image = request.FILES['profile_picture']
        profile.save()
        return JsonResponse({'image_url': profile.image.url})
    return JsonResponse({'error': 'Invalid request'}, status=400)


class CustomPasswordChangeView(AllauthPasswordChangeView, LoginRequiredMixin):
    """
    Django-allauth view for changing the user's password.
    """

    def get_success_url(self):
        # Overrides the default success_url to redirect to the user's profile
        return reverse('profiles:user-profile', kwargs={'pk': self.request.user.pk})


class AccountDeactivateView(LoginRequiredMixin, View):
    """
    View to request account deactivation.
    """
    template_name = 'account_deactivate.html'
    email_subject_template = 'account/email/account_deactivation_subject.txt'
    email_message_template = 'account/email/account_deactivation_message.txt'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Generate a one-time use token and send an email to the user
        user = request.user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode())

        # Create a URL for the deactivation link
        deactivate_url = reverse(
            'profiles:account-deactivate-confirm', kwargs={'uidb64': uid, 'token': token})
        deactivate_url = request.build_absolute_uri(deactivate_url)

        # Send the email containing the deactivation link
        self.send_deactivation_email(user.email, deactivate_url)
        
        # Return to the 'account_deactivate_mail_send' page
        return render(request, 'account_deactivate_mail_send.html')

    def send_deactivation_email(self, user_email, deactivate_url):
        """
        Send an email to the user with the deactivation link.
        """
        subject = render_to_string(self.email_subject_template)
        message = render_to_string(self.email_message_template, {
            'deactivate_url': deactivate_url,
        })
        email = EmailMessage(subject, message, to=[user_email])
        email.send()
