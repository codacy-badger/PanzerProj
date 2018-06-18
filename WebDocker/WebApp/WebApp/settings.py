"""
Django settings for WebApp project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

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
]

AUTHENTICATION_BACKENDS = (
    # social
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.vk.VKOAuth2',
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # social
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'WebApp.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'WebApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fitness_db',
        'USER': 'fitness_admin',
        'PASSWORD': 'veryhardpass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
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
LOGIN_REDIRECT_URL = 'auth-creating'

# OAuth data
SOCIAL_AUTH_VK_OAUTH2_KEY = '6605485'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'f0Njvt28fiKeo3nwXK4r'

SOCIAL_AUTH_FACEBOOK_KEY = '1088284781252797'
SOCIAL_AUTH_FACEBOOK_SECRET = 'be266e43619a9b62bae1e4524f093f21'

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

