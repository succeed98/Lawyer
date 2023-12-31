"""
Django settings for firm project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from decouple import config
import socket
# socket.getaddrinfo('app.minkahpremo.com', 80)
# from decouple import config


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "jhgfdxsdfgyhujikojhgvfcdrftgyhjbvcfdre567yuhjb"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','bfb6-102-176-65-153.ngrok.io']



# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'lawyers', 'cases',
    'documents', 'accounts',
    'crispy_forms',
    'rest_framework', 'timezone_field',
    'django_forms_bootstrap', 'wills', 'bootstrap_datepicker_plus', "bootstrap4", 'corsheaders','notify','mathfilters',
    'principles', 'background_task', 'django_filters', 'widget_tweaks', 'clients', 'ajax_select', 'schedules', 'visitors', 'import_export',
    'correspondents', 'resources', 'comment','django_otp',

    'ckeditor',
    'tinymce',


]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


ROOT_URLCONF = 'firm.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'cases.context_processors.user_messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },

]

WSGI_APPLICATION = 'firm.wsgi.application'




##### Project-specific settings









CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"




AUTHENTICATION_BACKENDS = (

    'django.contrib.auth.backends.ModelBackend',


)


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'minkahtest',
        'USER': 'postgres',
        'PASSWORD': 'jkm054',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'minka',
#         'USER': 'postgres',
#         'PASSWORD': 'jkm054',
#         'HOST': 'localhost',
#         'PORT': '5432',
#      }
# }





# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'test_db',
#         'USER': 'super',
#         'PASSWORD': 'mangafoxhydration',
#         'HOST': 'skboafoandco-1753.postgres.pythonanywhere-services.com',
#         'PORT': 11753,
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'lawyers.User'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static")

# ]
VENV_PATH = os.path.join(BASE_DIR)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "mail.integrisgh.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "mpobbapp@integrisgh.com"
EMAIL_HOST_PASSWORD = "M1nk@hApp2021"
DEFAULT_FROM_EMAIL = "Chambers Management Suite <mpobbapp@integrisgh.com>"



BACKGROUND_TASK_RUN_ASYNC = True

# channels



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

MESSAGES_TO_LOAD = 30

CORS_ORIGIN_ALLOW_ALL=True




NOTIFY_SOFT_DELETE=True

NOTIFY_NF_LIST_CLASS_SELECTOR = ".notifications"

NOTIFY_SINGLE_NF_CLASS_SELECTOR =".notifications"
NOTIFY_NF_BOX_CLASS_SELECTOR= ".notification-box-list"

NOTIFY_SINGLE_NF_BOX_CLASS_SELECTOR= ".notification-box"
NOTIFY_MARK_NF_CLASS_SELECTOR =".mark-notification"

NOTIFY_MARK_ALL_NF_CLASS_SELECTOR =".mark-all-notifications"

NOTIFY_READ_NOTIFICATION_CSS= "read"
NOTIFY_UNREAD_NOTIFICATION_CSS= "unread"
NOTIFY_DELETE_NF_CLASS_SELECTOR =".delete-notification"

NOTIFY_UPDATE_TIME_INTERVAL =5000



import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://70d7fd8d106749c7ac789fd53afb5b9b@o424573.ingest.sentry.io/5356523",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)



try:
    from .local_settings import *
except ImportError:
    pass
