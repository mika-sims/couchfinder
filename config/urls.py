from django.contrib import admin
from django.urls import path, include


from profiles.views import CustomPasswordChangeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),  # main app urls
    path(
        "accounts/password/change/",
        CustomPasswordChangeView.as_view(),
        name="change-password",
    ),
    path("accounts/", include("allauth.urls")),  # django-allauth urls
    path(
        "profiles/", include("profiles.urls", namespace="profiles")
    ),  # profiles app urls
]
