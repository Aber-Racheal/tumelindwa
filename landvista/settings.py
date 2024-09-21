import dj_database_url
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-=ao5v!so%6#%d@uncrf%uze@qpa1!frn6j&g)*^ix-5nonac=7'
GOOGLE_MAPS_API_KEY= 'AIzaSyBBYsZVdFOBv3is6gNS3SbHr_xWY4pkpV8'
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
    'feedback',
    'location',
    'authentication',
    'django.contrib.sites',
    'corsheaders',
    'flood_risk',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'landvista.urls'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

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

WSGI_APPLICATION = 'landvista.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

if not os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", '')
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", '')
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", '')
REDIRECT_URI = os.environ.get("REDIRECT_URI", '')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
