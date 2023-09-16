from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='user-profile'),
    path('profile-update/<int:pk>/',
         views.ProfileUpdateView.as_view(), name='profile-update'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('account-deactivate/', views.AccountDeactivateView.as_view(),
         name='account-deactivate'),
    path('account-deactivate-confirm/<str:uidb64>/<str:token>/',
         views.AccountDeactivateConfirmView.as_view(), name='account-deactivate-confirm'),
]
