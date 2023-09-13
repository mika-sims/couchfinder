from django.urls import path
from profiles.views import ProfileDetailView, ProfileUpdateView

app_name = 'profiles'

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='user-profile'),
    path('profile-update/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),
]