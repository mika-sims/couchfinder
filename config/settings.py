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
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Project Secret Key
SECRET_KEY = os.environ.get("SECRET_KEY")

# Allowed host/domain names to access the project
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "couchfinder-5f774dee7c25.herokuapp.com"]

# Debug Mode
DEBUG = os.environ.get("DEBUG")

# Installed packages (or modules) and apps for the project
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # Third party app. Has to be placed before 'django.contrib.staticfiles'
    "cloudinary_storage",
    "django.contrib.staticfiles",
    "phonenumber_field",
    # Third party apps
    "cloudinary",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "crispy_bootstrap5",
    "cities_light",
    # Project apps
    "main",
    "authentication",
    "profiles",
    "reviews",
]

# Configuration for the crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# list of middleware classes that process requests and responses
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Account middleware for django-allauth
    "allauth.account.middleware.AccountMiddleware",
]

# Project root URL configuration module
ROOT_URLCONF = "config.urls"

# Configuration for  the template engine used for
# rendering HTML templates and static files
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Location of the WSGI (Web Server Gateway Interface) application object
WSGI_APPLICATION = "config.wsgi.application"


# Database
DATABASES = {
    # Default database configuration
    "default": dj_database_url.parse(
        os.environ.get("DEFAULT_DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    ),
}


# Password validation rules for users when creating or changing passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Authentication backends used by the project
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Authentication user model
AUTH_USER_MODEL = "authentication.User"

# Site ID for the project
SITE_ID = 1

# django-allauth configuration
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
LOGIN_REDIRECT_URL = "main:homepage"
LOGOUT_REDIRECT_URL = "main:homepage"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_SIGNUP_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 3000
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_VERIFICATION = False
SOCIALACCOUNT_EMAIL_REQUIRED = False

# Override default forms for django-allauth
ACCOUNT_FORMS = {
    "signup": "authentication.forms.CustomSignupForm",
}

# Email verification configuration
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = os.environ.get("EMAIL_PORT")
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Default language
LANGUAGE_CODE = "en-us"

# Default time zone
TIME_ZONE = "UTC"

# Activate Django's translation system
USE_I18N = True

# Activate Django's timezone support
USE_TZ = True


# Static files storage settings (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_STORAGE = "cloudinary_storage.storage.StaticHashedCloudinaryStorage"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media files storage settings (Images, Videos, Audio)
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Default primary key field type for models
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
