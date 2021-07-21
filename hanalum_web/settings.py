"""
Django settings for hanalum_web project.
"""

import json
import os
from pathlib import Path

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG') == 'TRUE'
USE_DOCKER = os.environ.get('USE_DOCKER') == 'TRUE'

SITE_ID = 1

ALLOWED_HOSTS = ['34.220.59.114', '127.0.0.1', 'alpha.hanalum.kr', 'hanalum.kr']

# 유저모델 재설정
AUTH_USER_MODEL = "users.User"

# 로그인 실패시 URL
LOGIN_URL = "/"

"""이메일 설정"""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_HOST_USER = EMAIL_ADDRESS
MAIL_USERNAME = EMAIL_ADDRESS
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SERVER_EMAIL = EMAIL_ADDRESS
DEFAULT_FORM_MAIL = os.environ.get('DEFAULT_FORM_MAIL')
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

""" summernote setting """
SUMMERNOTE_CONFIG = {
    'iframe': False,
    'summernote': {
        'airMode': False,
        'width': '100%',
        'height': '480',
        'lang': 'ko-KR',
    },
    'attachment_require_authentication': True,
    'disable_attachment': False,
    'attachment_absolute_uri': False,
    'css_for_inplace': (
    ),
    'js_for_inplace': (
    ),
    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css',
    ),
    'codemirror': {
        'mode': 'htmlmixed',
        'lineNumbers': 'true',
        'theme': 'monokai',
    },
    'lazy': True,
}

ADMINLTE_SETTINGS = {
    'search_form': True,
    'navigation_expanded': False,

    'show_apps': [
        'main',
        'boards',
        'articles',
        'notices',
        'hanmaum',
        'comments',
        'hashtags',
        'history',
        'users',
        'joha',
        'sites'
    ],
    'main_navigation_app': 'django_admin_settings',
}


CUSTOM_APPS = [
    'users',
    'api',
    'articles',
    'boards',
    'comments',
    'hanmaum',
    'main',
    'notices',
    'hashtags',
    'history',
    'joha',
    'policies',
]

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
    'bootstrap5',
    'django_summernote',
    'fontawesome_5',
    'sass_processor',
    'django_inlinecss',
    'webpack_loader',
] + CUSTOM_APPS

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
            "libraries": {
                "comment_policy_tags": "comments.templatetags.comment_policy_tags",
            }
        },
    },
]

SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'static')
SASS_OUTPUT_STYLE = 'compact'

WSGI_APPLICATION = "hanalum_web.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('POSTGRES_NAME'),
        "USER": os.environ.get('POSTGRES_USER'),
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD'),
        "HOST": "db",
        "PORT": os.environ.get('POSTGRES_PORT'),
    }
} if USE_DOCKER else {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "node_modules/"),
    os.path.join(BASE_DIR, 'assets'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/', # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        'LOADER_CLASS': 'webpack_loader.loader.WebpackLoader',
    }
}
