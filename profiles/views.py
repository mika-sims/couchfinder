from django.contrib.auth import get_user_model, logout
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import View, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordChangeView as AllauthPasswordChangeView
from cities_light.models import Region, City

from .models import Profile
from . import forms
from reviews.forms import ReviewForm
from reviews.models import Review


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

    def get(self, request, *args, **kwargs):
        # Get the 'pk' parameter from the URL
        user_pk = self.kwargs.get('pk')

        # Retrieve the user associated with the profile
        user = get_object_or_404(get_user_model(), pk=user_pk)

        # Get the reviews
        try:
            if user == request.user:
                reviews = Review.objects.filter(profile=request.user.profile)
            else:
                reviews = Review.objects.filter(profile=user.profile)
        except Review.DoesNotExist:
            reviews = None

        return render(request, 'profile_details.html', {
            'profile': user.profile,
            'review_form': ReviewForm(),
            'reviews': reviews,
        })

    def post(self, request, *args, **kwargs):
        # Get the 'pk' parameter from the URL
        user_pk = self.kwargs.get('pk')

        # Retrieve the user associated with the profile
        user = get_object_or_404(get_user_model(), pk=user_pk)

        # Get the review form
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            # Create the review object but don't save it yet
            review = review_form.save(commit=False)

            # Assign the current user to the review
            review.user = request.user

            # Assign the review to the profile
            review.profile = user.profile

            # Save the review to the database
            review.save()
        else:
            review_form = ReviewForm()

        return render(request, 'profile_details.html', {
            'profile': user.profile,
            'review_form': review_form,
        })


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


def get_regions(request):
    country_id = request.GET.get('country_id')
    regions = Region.objects.filter(country_id=country_id)
    data = {
        'regions': [{'id': region.id, 'name': region.name} for region in regions]
    }
    return JsonResponse(data)


def get_cities(request):
    region_id = request.GET.get('region_id')
    cities = City.objects.filter(region_id=region_id)
    data = {
        'cities': [{'id': city.id, 'name': city.name} for city in cities]
    }
    return JsonResponse(data)


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
                messages.error(
                    request, 'Invalid link. Please request deactivation again.')
                return redirect('account_login')

        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            messages.error(
                request, 'Invalid link. Please request deactivation again.')
            return redirect('account_login')


class AccountDeactivateDoneView(View):
    """
    View to display a success message after account deactivation.
    """
    template_name = 'account_deactivate_done.html'

    def get(self, request):
        return render(request, self.template_name)


class ProfileSearchView(View):
    template_name = 'profile_search.html'

    def get(self, request):
        form = forms.ProfileForm(request.GET)
        profiles = Profile.objects.all().exclude(user=request.user)

        if form.is_valid():
            couch_status = form.cleaned_data.get('couch_status')
            country = form.cleaned_data.get('country')
            region = form.cleaned_data.get('region')
            city = form.cleaned_data.get('city')

            if couch_status:
                profiles = profiles.filter(couch_status=couch_status)
            if country:
                profiles = profiles.filter(country=country)
            if region:
                profiles = profiles.filter(region=region)
            if city:
                profiles = profiles.filter(city=city)
        else:
            form = forms.ProfileForm()
            # Display message if no profiles were found
            messages.error(request, 'No profiles found.')

        context = {
            'form': form,
            'profiles': profiles,
        }

        return render(request, self.template_name, context)
