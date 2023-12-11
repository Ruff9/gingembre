"""
Django settings for gingembre project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import io
import os
from urllib.parse import urlparse

import environ
from google.cloud import secretmanager

env = environ.Env(DEBUG=(bool, False))

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Setup google app engine
# env_file = os.path.join(BASE_DIR, ".env")

# if os.path.isfile(env_file):
#     # Use a local secret file, if provided
#     env.read_env(env_file)

# elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
#     # Pull secrets from Secret Manager
#     project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

#     client = secretmanager.SecretManagerServiceClient()
#     settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
#     name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
#     payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

#     env.read_env(io.StringIO(payload))
# else:
#     raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")


# False if not in os.environ because of casting above
DEBUG = env('DEBUG')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')


if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Setup google app engine
# if DEBUG:
#     ALLOWED_HOSTS = ['*']
# else:
#     ALLOWED_HOSTS = ['annular-ocean-407615.ew.r.appspot.com']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'compressor',
    'messenger',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

ROOT_URLCONF = 'gingembre.urls'

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

# WSGI_APPLICATION = 'gingembre.wsgi.application'

ASGI_APPLICATION = "gingembre.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/db.sqlite3',
        'TEST': {
            'NAME': BASE_DIR + '/test_db.sqlite3',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'messenger/static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Scss compilation setup
# https://lukeplant.me.uk/blog/posts/django-sass-scss-without-nodejs-or-build-step/

COMPRESS_ROOT = 'messenger/static/'
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
