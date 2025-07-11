import os
import stat
from datetime import timedelta
from pathlib import Path

from environ import Env

# Path Settings
BASE_DIR = Path(__file__).resolve().parent.parent
env = Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

# Core Django Settings
SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")
ROOT_URLCONF = "server.urls"
WSGI_APPLICATION = "server.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security Settings
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

# Host Settings
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

# CORS Settings
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_METHODS = env.list("CORS_ALLOW_METHODS")
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS")
CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS")
CORS_EXPOSE_HEADERS = env.list("CORS_EXPOSE_HEADERS")
CORS_ALLOW_HEADERS = env.list("CORS_ALLOW_HEADERS")

# Application Definition
DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)

PROJECT_APPS = (
)

THIRD_PARTY_APPS = (
    "corsheaders",
    "ninja",
    "redis",
    "django_redis",
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

# Middleware Configuration
MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

# Template Configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# Database Configuration
DATABASES = {
    "default": {
        "ENGINE": env.str("DATABASE_ENGINE"),
        "NAME": env.str("DATABASE_NAME"),
        "USER": env.str("DATABASE_USER"),
        "PASSWORD": env.str("DATABASE_PASSWORD"),
        "HOST": env.str("DATABASE_HOST"),
        "PORT": env.int("DATABASE_PORT"),
    },
}

# Cache configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "shared.serializers.redis_serializer.ApplicationRedisSerializer",
        },
        "TIMEOUT": 300,
        "KEY_PREFIX": "django_cache",
    }
}

# Authentication Settings
# AUTH_USER_MODEL = "accounts.Account"
AUTH_PASSWORD_VALIDATORS = (
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
)

# Internationalization Settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Sofia"
USE_I18N = True
USE_TZ = True

# Static Files Settings
STATIC_URL = "/static/"
STATIC_ROOT = "/staticfiles"
STATICFILES_DIRS = []
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

# Logging Configuration
LOGS_DIR = BASE_DIR / "logs"
if not os.path.exists('logs'):
    os.mkdir('logs')

# Loki Configuration
LOKI_URL = os.environ.get("LOKI_URL", "http://loki:3100")
GRAFANA_URL = os.environ.get("GRAFANA_URL", "http://grafana:3000")
