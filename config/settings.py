"""
Django settings for the "Couch Finder" Project.

Django Version: 4.2.4.
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
from pathlib import Path

# Get the environment variables if they exist
if os.path.exists("env.py"):
    import env

# Base Directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Project Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY')

# Allowed host/domain names to access the project
ALLOWED_HOSTS = []


# Installed packages (or modules) and apps for the project
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
]

# Project root URL configuration module
ROOT_URLCONF = 'config.urls'

# Configuration for  the template engine used for
# rendering HTML templates and static files
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Location of the WSGI (Web Server Gateway Interface) application object
WSGI_APPLICATION = 'config.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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


# Default language
LANGUAGE_CODE = 'en-us'

# Default time zone
TIME_ZONE = 'UTC'

# Activate Django's translation system
USE_I18N = True

# Activate Django's timezone support
USE_TZ = True


# Static files (CSS, JavaScript, Images) location
STATIC_URL = 'static/'

# Default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
