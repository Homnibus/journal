"""
Django settings for rescodex project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "+7tc6*)=+zg=3k-+rl#n%dra34e!ir=)x_o-(#3_9v8ikm-=!6"

# SECURITY WARNING: don't run with debug turned on in production!
if "runserver" in sys.argv:
  DEBUG = True

if "runserver" in sys.argv:
  ALLOWED_HOSTS = ["*"]
else:
  ALLOWED_HOSTS = ["www.rescodex.com"]

# Application definition

INSTALLED_APPS = [
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",
  "rs_back_end",
  "rest_framework",
  "rest_framework.authtoken",
  "django_filters",
  "guardian",
  "corsheaders",
]

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.locale.LocaleMiddleware",
  "corsheaders.middleware.CorsMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.contrib.messages.middleware.MessageMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",
  "rs_back_end.middleware.PutAndDeleteParsingMiddleware",
  "rs_back_end.middleware.RequestExceptionHandler",
]

ROOT_URLCONF = "rescodex.urls"

TEMPLATES = [
  {
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {
      "context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "django.template.context_processors.i18n",
      ]
    },
  }
]

AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
  'guardian.backends.ObjectPermissionBackend',
)

WSGI_APPLICATION = "rescodex.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "OPTIONS": {"options": "-c search_path=public"},
    "NAME": "djournald2K001",
    "USER": "journaldadm",
    "PASSWORD": "admin",
    "HOST": "localhost",
    "PORT": "12200",
  }
}

if "test" in sys.argv or "test_coverage" in sys.argv:
  DATABASES = {
    "default": {
      "ENGINE": "django.db.backends.sqlite3",
      "NAME": ":memory:",
      "TEST": {},
    }
  }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
  ],
  'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
  'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
if "runserver" in sys.argv:
  CORS_ORIGIN_WHITELIST = ["http://localhost:4200", ]

AUTH_PASSWORD_VALIDATORS = [
  {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
  {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
  {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
  {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "/connexion"
LOGIN_REDIRECT_URL = "/"

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

LOCALE_PATHS = (os.path.join(BASE_DIR, "rs_back_end/locale"),)

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = "/static/"

LOGGING = {
  "version": 1,
  "disable_existing_loggers": True,
  "formatters": {
    "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}
  },
  "handlers": {
    "default": {
      "level": "DEBUG",
      "class": "logging.handlers.RotatingFileHandler",
      "filename": "logs/mylog.log",
      "maxBytes": 1024 * 1024 * 5,  # 5 MB
      "backupCount": 5,
      "formatter": "standard",
    },
    "request_handler": {
      "level": "DEBUG",
      "class": "logging.handlers.RotatingFileHandler",
      "filename": "logs/django_request.log",
      "maxBytes": 1024 * 1024 * 5,  # 5 MB
      "backupCount": 5,
      "formatter": "standard",
    },
    "console": {
      "level": "DEBUG",
      "class": "logging.StreamHandler",
      "formatter": "standard",
    },
  },
  "root": {"handlers": ["default"], "level": "DEBUG"},
  "loggers": {
    "django": {"handlers": ["console"], "propagate": True},
    "django.request": {
      "handlers": ["request_handler"],
      "level": "DEBUG",
      "propagate": False,
    },
  },
}
