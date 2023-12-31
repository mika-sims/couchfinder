from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("profile/<int:pk>/", views.ProfileDetailView.as_view(), name="user-profile"),
    path(
        "profile-update/<int:pk>/",
        views.ProfileUpdateView.as_view(),
        name="profile-update",
    ),
    path("get_regions/", views.get_regions, name="get_regions"),
    path("get_cities/", views.get_cities, name="get_cities"),
    path("upload_image/", views.upload_image, name="upload_image"),
    path(
        "account-deactivate/",
        views.AccountDeactivateView.as_view(),
        name="account-deactivate",
    ),
    path(
        "account-deactivate-confirm/<str:uidb64>/<str:token>/",
        views.AccountDeactivateConfirmView.as_view(),
        name="account-deactivate-confirm",
    ),
    path(
        "account-deactivate-done/",
        views.AccountDeactivateDoneView.as_view(),
        name="account-deactivate-done",
    ),
    path("profile-search/", views.ProfileSearchView.as_view(), name="profile-search"),
    path(
        "update-review/<int:pk>/",
        views.UpdateReviewView.as_view(),
        name="update-review",
    ),
    path(
        "delete-review/<int:pk>/",
        views.DeleteReviewView.as_view(),
        name="delete-review",
    ),
]
