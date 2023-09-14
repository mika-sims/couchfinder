from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordChangeView as AllauthPasswordChangeView

from .models import Profile
from .forms import ProfileForm


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
    form_class = ProfileForm
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