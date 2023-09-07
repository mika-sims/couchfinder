"""
Django settings for the "Couch Finder" Project.

Django Version: 3.2 (LTS) 
Note: This version of the Django is compatible with ElephantSQL postgresql database.
=========================================================================
This project is exclusively developed for educational purposes, 
with its primary intention being to serve as an instructional tool. 
It has been created specifically to fulfill the requirements of the 
Full-Stack Software Development course offered by Code Institute.

Project Start Date:  03/09/2023

Project Developer: Mikail Şimşek

Contact Information: mikailsimsek.trb@gmail.com
"""


import os
import dj_database_url
from pathlib import Path

# Get the environment variables if they exist
if os.path.exists("env.py"):
    import env

# Base Directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Template Directory of the project
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Project Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY')

# Allowed host/domain names to access the project
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# Debug Mode
DEBUG = os.environ.get('DEBUG')

# Installed packages (or modules) and apps for the project
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Third party app. Has to be placed before 'django.contrib.staticfiles'
    'cloudinary_storage',
    'django.contrib.staticfiles',

    # Third party apps
    'cloudinary',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Project apps
    'main',
]

# list of middleware classes that process requests and responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Account middleware for django-allauth
    "allauth.account.middleware.AccountMiddleware",
]

# Project root URL configuration module
ROOT_URLCONF = 'config.urls'

# Configuration for  the template engine used for
# rendering HTML templates and static files
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `django-allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

# Location of the WSGI (Web Server Gateway Interface) application object
WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    # Default database configuration
    'default': dj_database_url.parse(os.environ.get('DEFAULT_DATABASE_URL'),
                                     conn_max_age=600,
                                     conn_health_checks=True,
                                     ),
    # Test database configuration
    'test': dj_database_url.parse(os.environ.get('TEST_DATABASE_URL'),
                                  conn_max_age=600,
                                  conn_health_checks=True,
                                  ),
}


# Password validation rules for users when creating or changing passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Authentication backends used by the project
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Default language
LANGUAGE_CODE = 'en-us'

# Default time zone
TIME_ZONE = 'UTC'

# Activate Django's translation system
USE_I18N = True

# Activate Django's timezone support
USE_TZ = True


# Static files storage settings (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files storage settings (Images, Videos, Audio)
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
