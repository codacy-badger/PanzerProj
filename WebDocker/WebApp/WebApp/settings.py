"""
Django settings for WebApp project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@h(=a+jjxy_-$mgv&rd^0cun003s^w!7-k9%rbkdv3np7cpb-3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = '*'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'FitnessPersonalArea.apps.FitnesswebConfig',
    # social
    'social_django',
    # tags
    'taggit',
    # geolocation
    'django.contrib.gis',
]

AUTHENTICATION_BACKENDS = (
    # social
    'social_core.backends.twitter.TwitterOAuth', # for twitter oauth
    'social_core.backends.vk.VKOAuth2', # for VK oauth
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # social
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'WebApp.urls'

FILE_UPLOAD_MAX_MEMORY_SIZE = 15000000

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # social
                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',  # <--
            ],
        },
    },
]

WSGI_APPLICATION = 'WebApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'fitness_db',
        'USER': 'fitness_admin',
        'PASSWORD': 'veryhardpass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# доступные языки для переводов
LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'Localisations'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = "/static/admin"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# social
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
# перенаправление после логина через соц-сети
LOGIN_REDIRECT_URL = 'success_login'

# OAuth data
SOCIAL_AUTH_VK_OAUTH2_KEY = '6605485'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'f0Njvt28fiKeo3nwXK4r'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '429925075232-9tdk0pts8mfu1m3q3iofe0h8u1605h5n.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'zmNvKL8TNo77X__Qv4CCcSG1'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    #'social_core.pipeline.debug.debug', # uncomment to print debug
)

SOCIAL_AUTH_TWITTER_KEY = 'P9jlutAT1baIhGnb3MK2RYtd0'
SOCIAL_AUTH_TWITTER_SECRET = 'cu1nkYnOxvZjPmZHewNHJX63hu2QarC5pDUo6Tsgc2r92eqhZ6'


# `срок годности` cookie
# SESSION_COOKIE_AGE = 2*3600

# CELERY
# Celery settings for rabbitmq
BROKER_URL = 'amqp://localhost:5672'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TIMEZONE = 'Europe/Minsk'

