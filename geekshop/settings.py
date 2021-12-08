"""
Django settings for geekshop project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
f
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import json
import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w=asr$9a21u%tj3!vuug9m7$6(r6prs+aiwxl6*i_9c%ei44pq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',
                 'localhost',
                 'django.radif.ru',
                 'www.django.radif.ru',
                 ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
    'authapp',
    'basketapp',
    'adminapp',
    'social_django',
    'ordersapp.apps.OrdersappConfig',
]

MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',  # кэширование всего сайта

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',

    # 'django.middleware.cache.FetchFromCacheMiddleware',  # кэширование всего сайта
]

if DEBUG:
    INSTALLED_APPS.extend([
        'debug_toolbar',
        'template_profiler_panel',
        'django_extensions',
    ])
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda x: True,
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'template_profiler_panel.panels.template.TemplateProfilerPanel',
    ]

ROOT_URLCONF = 'geekshop.urls'

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
                'mainapp.context_processors.get_categories',  # пример контекстного процессора
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'geekshop.wsgi.application'

SECRETS_FILE = '/var/sec/geekshop__settings.json'
EMAIL = {}
SOCIAL_AUTH = {}
DATABASE = {}
if os.path.exists(SECRETS_FILE):
    with open(SECRETS_FILE, 'r') as f:
        LOCAL_SETTINGS = json.load(f)
        EMAIL = LOCAL_SETTINGS.get('EMAIL', '')
        SOCIAL_AUTH = LOCAL_SETTINGS.get('SOCIAL_AUTH', '')
        DATABASE = LOCAL_SETTINGS.get('DATABASE', '')

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE.get('NAME', ''),
        'USER': DATABASE.get('USER', ''),
        'PASSWORD': DATABASE.get('PASSWORD', ''),
        'HOST': 'localhost',
        # 'PORT': '5432',
    }
}

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

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

USERS_AVATARS = 'users_avatars'

AUTH_USER_MODEL = 'authapp.ShopUser'

JSON_PATH = 'json'

LOGIN_URL = '/auth/login/'

# Настройки почты:
DOMAIN_NAME = 'https://django.radif.ru'

USER_EXPIRES_TIMEDELTA = timedelta(hours=48)

EMAIL_HOST = EMAIL.get('HOST', '')
EMAIL_PORT = EMAIL.get('PORT', '')
EMAIL_HOST_USER = EMAIL.get('HOST_USER', '')  # i@radif.ru'
EMAIL_HOST_PASSWORD = EMAIL.get('HOST_PASSWORD', '')
EMAIL_USE_SSL = True

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# # Настройки почты для тестирования:
# DOMAIN_NAME = 'http://localhost:8000'
#
# USER_EXPIRES_TIMEDELTA = timedelta(hours=48)
#
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = '25'
# EMAIL_HOST_USER = 'django@geekshop.local'
# EMAIL_HOST_PASSWORD = 'geekshop'
# EMAIL_USE_SSL = False
# # Для работы с реального хоста
# # EMAIL_USE_TLS = True
#
# # вариант sudo python3 -m smtpd -n -c DebuggingServer localhost:25
# # EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = None, None
#
# # вариант логирования сообщений почты в виде файлов вместо отправки
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = 'tmp/email-messages/'

# social auth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# SOCIAL_AUTH_VK_OAUTH2_KEY = os.environ.setdefault('SOCIAL_AUTH_VK_OAUTH2_KEY', VK['SOCIAL_AUTH_VK_OAUTH2_KEY'])
SOCIAL_AUTH_VK_OAUTH2_KEY = SOCIAL_AUTH.get('VK_OAUTH2_KEY', '')
SOCIAL_AUTH_VK_OAUTH2_SECRET = SOCIAL_AUTH.get('OAUTH2_SECRET', '')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = SOCIAL_AUTH.get('GOOGLE_OAUTH2_KEY', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = SOCIAL_AUTH.get('GOOGLE_OAUTH2_SECRET', '')

LOGIN_ERROR_URL = '/auth/login/'

SOCIAL_AUTH_VK_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_VK_OAUTH2_SCOPE = [
    'email', 'bdate', 'sex', 'about'
]

SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'email',
    'profile',
    'openid',
    'https://www.googleapis.com/auth/plus.login',
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.create_user',
    'authapp.pipeline.save_user_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

if os.name == 'posix':
    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 120
    CACHE_MIDDLEWARE_KEY_PREFIX = 'geekshop'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

LOW_CACHE = True
