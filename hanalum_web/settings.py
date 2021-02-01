"""
Django settings for hanalum_web project.
"""

import json
import os
from pathlib import Path

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

secret_file = os.path.join(BASE_DIR, "secrets.json")  # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secret_text = json.loads(f.read())


def get_secret(setting, secrets=secret_text):
    """
    secrets.json으로부터, 값을 가져오는 함수입니다.
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg) from KeyError(error_msg)


SITE_ID = 1

SECRET_KEY = get_secret("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

# 유저모델 재설정
AUTH_USER_MODEL = "user.User"

# 로그인 실패시 URL
LOGIN_URL = "/"

"""이메일 설정"""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = "contacthanmin01@gmail.com"
EMAIL_HOST_USER = EMAIL_ADDRESS
EMAIL_HOST_PASSWORD = get_secret("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SERVER_EMAIL = EMAIL_ADDRESS
DEFAULT_FORM_MAIL = "contacthanmin01"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

""" 메세지 프레임워크 클래스 설정 """
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

""" summernote load issue """
X_FRAME_OPTIONS = 'SAMEORIGIN'

INSTALLED_APPS = [
    'adminlteui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'treebeard',
    "bootstrap5",
    "django_summernote",
    "api",
    "article",
    "board",
    "hanmaum",
    "main",
    "menu",
    "policy",
    "user",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hanalum_web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "hanalum_web.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/")
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
