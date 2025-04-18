"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-nhyr5kxl-0jw0z0=#!9uhj50aq+b)q@yb(jh2%o36ooyr9m*55'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'api.User'

ASGI_APPLICATION = "core.asgi.application"

# Application definition

INSTALLED_APPS = [
    "channels",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "corsheaders",
    "api",
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middleware.middlewares.LogErroMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("NOME_DO_BANCO"),
        'USER': os.getenv("USUARIO_DO_BANCO"),
        'PASSWORD': os.getenv("SENHA_DO_BANCO"),
        'HOST': os.getenv("HOST_DO_BANCO"),
        'PORT': os.getenv("PORTA_DO_BANCO"),
        "OPTIONS": {
            "connect_timeout": 10,
        },
        "ATOMIC_REQUESTS": True,
    }
}
# Configuração do Redis com o Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Recife'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    # Configuração da paginação da API.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # Configuração do Swagger
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Aceita data e hora no formato brasileiro
    'DATE_FORMAT': "%d-%m-%Y",
    'DATETIME_FORMAT': "%d-%m-%Y %H:%M",
    'DATE_INPUT_FORMATS': ["%d-%m-%Y"],
    'DATETIME_INPUT_FORMATS': ["%d-%m-%Y %H:%M"],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=2),
    'CANCEL_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_USER_MODEL': 'api.User',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'EasyDrive',
    'DESCRIPTION': 'Esta é a documentação da API EasyDrive, um sistema de gerenciamento de alugueis de veiculos.',
    'VERSION': '1.0.0',
    'TERMS_OF_SERVICE': 'github.io//RobsonFe',
    'CONTACT': {
        'name': 'Robson Ferreira',
        'email': 'robsonfe.dev@gmail.com',
    },
    'LICENSE': {
        'name': 'EULA License',
        'url': 'https://www.eula.com',
    },
    'SCHEMA_COERCE_PATH_PK_SUFFIX': True,
    'TAGS': [
        {'name': 'Usuário', 'description': 'Configurações referentes aos usuários do sistema'},
    ],
    'SORT_OPERATIONS': False,  # Mantém a ordem definida das tags
    'ENUM_NAME_OVERRIDES': {},  # Evita que o Spectacular gere categorias extras
    'SCHEMA_PATH_PREFIX': '/api/v1',  # Prefixo para os endpoints
    'ENUM_GENERATE_CHOICE_DESCRIPTION': True,
    'ENUM_SUFFIX': 'Type',
    'POSTPROCESSING_HOOKS': [
        # Esse hook filtra os endpoints que não possuem uma das tags permitidas
        'api.utils.allowed_tags.filter_endpoints_by_allowed_tags',
    ],
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    'SERVE_INCLUDE_SCHEMA': True,
    "COMPONENT_SPLIT_REQUEST": False,
}
