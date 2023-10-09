import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from profiles.views import CustomPasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),  # main app urls
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name='change-password'),
    path('accounts/', include('allauth.urls')), # django-allauth urls
    path('profiles/', include('profiles.urls', namespace='profiles')), # profiles app urls
]

# Static and media files location for development
if os.environ.get('DEBUG') == 'True':
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
