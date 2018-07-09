"""
Django settings for hc project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
# flake8: noqa
import os
import warnings
import dj_database_url
<<<<<<< HEAD
<<<<<<< HEAD
from decouple import config
=======
from decople import config
>>>>>>> [Feature #158174601] Update settings
=======
from decouple import config
>>>>>>> [Feature #158174601] Update settings spelling

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOST = "localhost"
SECRET_KEY = "---"
DEBUG = True
ALLOWED_HOSTS = []
DEFAULT_FROM_EMAIL = 'healthchecks@example.org'
USE_PAYMENTS = False


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'djmail',

    'hc.accounts',
    'hc.api',
    'hc.front',
    'hc.payments'
)


MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hc.accounts.middleware.TeamAccessMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'hc.accounts.backends.EmailBackend',
    'hc.accounts.backends.ProfileBackend'
)

ROOT_URLCONF = 'hc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'hc.payments.context_processors.payments'
            ],
        },
    },
]

WSGI_APPLICATION = 'hc.wsgi.application'
TEST_RUNNER = 'hc.api.tests.CustomRunner'


# Default database engine is SQLite. So one can just check out code,
# install requirements.txt and do manage.py runserver and it works
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './hc.sqlite',
    }
}

# You can switch database engine to postgres or mysql using environment
# variable 'DB'. Travis CI does this.
if os.environ.get("DB") == "postgres":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'hc',
            'USER': 'postgres',
            'TEST': {'CHARSET': 'UTF8'}
        }
    }

if os.environ.get("DB") == "heroku":
    DATABASES = {
        'default': dj_database_url.config(default=config('DATABASE_URL'))
    }

if os.environ.get("DB") == "mysql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'NAME': 'hc',
            'TEST': {'CHARSET': 'UTF8'}
        }
    }

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
SITE_ROOT = os.environ.get("SITE_ROOT", "http://localhost:8000")
=======
SITE_ROOT = os.environ.get['SITE_ROOT']
>>>>>>> [Feature #158174601] Enable site root to be picked from environment
=======
SITE_ROOT = "http://localhost:8000"
>>>>>>> [Feature #158174601] Add site root
=======
SITE_ROOT = os.environ.get('SITE_ROOT')
>>>>>>> [Feature #158174601] Update travis file
=======
SITE_ROOT = "http://localhost:8000"
>>>>>>> [Feature #158174601] Remove changes from travis
=======
SITE_ROOT = os.environ.get('SITE_ROOT')
>>>>>>> [Feature #158174601] Make changes to travis
=======
SITE_ROOT = "http://localhost:8000"
>>>>>>> [Feature #158174601] Remove changes from travis
=======
SITE_ROOT = os.environ.get('SITE_ROOT') or "http://localhost:8000"
>>>>>>> [Feature #158174601] Update settings
=======
SITE_ROOT = os.environ.get('SITE_ROOT', 'http://localhost:8000')
>>>>>>> [Feature #158174601] Fix remove shopify check
PING_ENDPOINT = SITE_ROOT + "/ping/"
PING_EMAIL_DOMAIN = HOST
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'static-collected')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
COMPRESS_OFFLINE = True

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
=======
EMAIL_BACKEND = "djmail.backends.default.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
>>>>>>> [Feature #158174601] Enable site root to be picked from environment
=======
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
=======
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
>>>>>>> [Feature #158174601] Fix remove shopify check
EMAIL_HOST = os.environ.get('EMAIL_HOST')
>>>>>>> [Feature #158174601] Update requirements.txt
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
<<<<<<< HEAD
<<<<<<< HEAD
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
=======
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
>>>>>>> [Feature #158174601] Enable site root to be picked from environment
=======
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
>>>>>>> [Feature #158174601] Update requirements.txt

# Slack integration -- override these in local_settings
SLACK_CLIENT_ID = None
SLACK_CLIENT_SECRET = None

# Pushover integration -- override these in local_settings
PUSHOVER_API_TOKEN = None
PUSHOVER_SUBSCRIPTION_URL = None
PUSHOVER_EMERGENCY_RETRY_DELAY = 300
PUSHOVER_EMERGENCY_EXPIRATION = 86400

# Twilio integration
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")


# Pushbullet integration -- override these in local_settings
PUSHBULLET_CLIENT_ID = None
PUSHBULLET_CLIENT_SECRET = None

if os.path.exists(os.path.join(BASE_DIR, "hc/local_settings.py")):
    from .local_settings import *
else:
    warnings.warn("local_settings.py not found, using defaults")
