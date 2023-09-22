from django.contrib.auth import get_user_model, logout
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import View, DetailView, UpdateView, ListView
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
        return super(ProfileUpdateView, self).form_valid(form)


def upload_image(request):
    # Upload the image and return the URL using a JSON response
    if request.method == 'POST' and request.FILES.get('profile_picture'):
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


class AccountDeactivateConfirmView(LoginRequiredMixin, View):
    """
    View to confirm account deactivation.
    """
    template_name = 'account_deactivate_confirm.html'
    success_url = 'profiles:account-deactivate-done'

    def get(self, request, uidb64, token):
        try:
            # Decode the UID and get the user
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)

            # Check if the token is valid
            if default_token_generator.check_token(user, token):
                # Deactivate the user's account
                user.is_active = False
                user.save()
                
                # Log out the user
                logout(request)

                # Redirect to the 'account_deactivated_done' page with success message
                messages.success(request, 'Your account has been deactivated.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Invalid link. Please request deactivation again.')
                return redirect('account_login')

        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            messages.error(request, 'Invalid link. Please request deactivation again.')
            return redirect('account_login')


class AccountDeactivateDoneView(View):
    """
    View to display a success message after account deactivation.
    """
    template_name = 'account_deactivate_done.html'

    def get(self, request):
        return render(request, self.template_name)


class ProfileSearchView(LoginRequiredMixin, ListView):
    model = Profile
    template = 'profile_search.html'
    context_object_name = 'profiles'
    form_class = forms.ProfileForm
    fields = ['couch_status', 'country', 'region', 'city']
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # Initialize queryset (excluding the user's own profile)
        queryset = Profile.objects.all().exclude(user=request.user)

        # Retrieve search parameters from the AJAX request
        first_name = request.GET.get('first_name', '')
        last_name = request.GET.get('last_name', '')
        couch_status = request.GET.get('couch_status', '')
        country = request.GET.get('country', '')
        region = request.GET.get('region', '')
        city = request.GET.get('city', '')

        # Apply filters based on the search parameters
        if first_name:
            queryset = queryset.filter(user__first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(user__last_name__icontains=last_name)
        if couch_status:
            queryset = queryset.filter(couch_status=couch_status)
        if country:
            queryset = queryset.filter(country__name__icontains=country)
        if region:
            queryset = queryset.filter(region__name__icontains=region)
        if city:
            queryset = queryset.filter(city__name__icontains=city)

        return render(request, 'profile_search.html', {'profiles': queryset})
