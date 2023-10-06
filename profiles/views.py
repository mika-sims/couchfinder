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
from friendship.models import Friend, FriendshipRequest
from friendship.exceptions import AlreadyExistsError

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

    def get(self, request, *args, **kwargs):
        # Get the 'pk' parameter from the URL
        user_pk = self.kwargs.get('pk')
        
        # Retrieve the user associated with the profile
        user = get_object_or_404(get_user_model(), pk=user_pk)
        
        # Get the friendship requests for both users
        friendship_requests = FriendshipRequest.objects.all()

        # Get all friends
        friends = Friend.objects.friends(user)
        
        return render(request, 'profile_details.html', {'profile': user.profile, 'friends': friends, 'friendship_requests': friendship_requests})


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
        return render(request, 'profile_search.html', {'profiles': queryset})


class SendFriendshipRequestView(LoginRequiredMixin, View):
    """
    View to send a friendship request to another user.
    """

    def post(self, request, *args, **kwargs):
        user_pk = self.kwargs.get('pk')
        from_user = request.user

        # Retrieve the user associated with the profile
        to_user = get_user_model().objects.get(pk=user_pk)

        # Check if the sender and recipient are the same user
        if from_user == to_user:
            messages.error(
                request, "You cannot send a friend request to yourself.")
        else:
            try:
                Friend.objects.add_friend(from_user, to_user)
                messages.success(
                    request, f"Friendship request sent to {to_user}")
            except AlreadyExistsError:
                messages.error(
                    request, f"Friendship request to {to_user} already exists")

        # Redirect to the sender's profile instead of the recipient's profile
        return redirect('profiles:user-profile', pk=from_user.pk)


class DisplayFriendshipRequestsView(LoginRequiredMixin, View):
    """
    View to fetch friendship requests received by the user as JSON
    and display them as notifications.
    """

    def get(self, request, *args, **kwargs):
        # Get the friendship requests received by the current user
        friendship_requests = FriendshipRequest.objects.filter(
            to_user=request.user)

        # Return the friendship requests as JSON
        data = {
            'friendship_requests': [{
                'id': request.from_user.pk,
                'from_user': request.from_user.get_full_name()
            }
                for request in friendship_requests
            ]
        }
        return JsonResponse(data)


class AcceptFriendshipRequestView(LoginRequiredMixin, View):
    """
    View to accept a friendship request.
    """

    def post(self, request, *args, **kwargs):
        # Get the 'pk' parameter from the URL
        user_pk = self.kwargs.get('pk')

        # Retrieve the user associated with the profile
        from_user = get_object_or_404(get_user_model(), pk=user_pk)

        # Get the friendship request
        friendship_request = get_object_or_404(
            FriendshipRequest,
            from_user=from_user,
            to_user=request.user
        )

        # Accept the friendship request
        friendship_request.accept()
        
        # Return a success message
        messages.success(request, f"You are now friends with {from_user}.")
        
        # Redirect to the sender's profile instead of the recipient's profile
        return redirect('profiles:user-profile', pk=from_user.pk)


class RejectFriendshipRequestView(LoginRequiredMixin, View):
    """
    View to reject a friendship request.
    """

    def post(self, request, *args, **kwargs):
        # Get the 'pk' parameter from the URL
        user_pk = self.kwargs.get('pk')

        # Retrieve the user associated with the profile
        from_user = get_object_or_404(get_user_model(), pk=user_pk)

        # Get the friendship request
        friendship_request = FriendshipRequest.objects.get(
            from_user=from_user, to_user=request.user)
        
        # Reject the friendship request
        friendship_request.reject()
        
        # Delete the friendship request
        friendship_request.delete()
        
        # Return a success message
        messages.success(
            request, f"You rejected the friendship request from {from_user}.")

        # Redirect to the user's profile
        return redirect('profiles:user-profile', pk=request.user.pk)


class FriendsListView(LoginRequiredMixin, View):
    """
    View to display the user's friends.
    """
    model = Profile
    template_name = 'friends_list.html'
    context_object_name = 'friends'
    paginate_by = 10
    
    def get(self, request, *args, **kwargs):
        # Get the user's friends
        friends = Friend.objects.friends(request.user)

        return render(request, 'friends_list.html', {'friends': friends})
    
class FriendshipRequestListView(LoginRequiredMixin, View):
    """
    View to display the user's friendship requests
    in a template.
    """
    model = Profile
    template_name = 'friendship_request_list.html'
    context_object_name = 'friendship_requests'
    paginate_by = 10
    
    def get(self, request, *args, **kwargs):
        # Get the 'pk' parameter from the URL
        user_pk = self.kwargs.get('pk')
        
        # Retrieve the user associated with the profile
        user = get_object_or_404(get_user_model(), pk=user_pk)
        
        # Get the user's friendship requests
        friendship_requests = FriendshipRequest.objects.filter(to_user=user)
        
        return render(request, 'friendship_request_list.html', {'friendship_requests': friendship_requests})