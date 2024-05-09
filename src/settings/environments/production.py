from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = [
    config("CLIENT_HOST", cast=str),
    config("SERVER_HOST", cast=str),
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{config('SERVER_HOST', cast=str)}",
    f"https://{config('CLIENT_HOST', cast=str)}",
]

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True


# CORS settings
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [f"https://{config('CLIENT_HOST', cast=str)}"]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("MYSQL_DB_NAME", cast=str),
        "USER": config("MYSQL_DB_USER", cast=str),
        "PASSWORD": config("MYSQL_DB_PASSWORD", cast=str),
        "HOST": config("MYSQL_DB_HOST", cast=str),
        "OPTIONS": {
            "sql_mode": "STRICT_TRANS_TABLES",
        },
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_ROOT = Path.joinpath(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# LOGGING settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}


# SMTP settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = config("EMAIL_HOST_USER", cast=str)
EMAIL_FROM_USER = config("EMAIL_HOST_USER", cast=str)
EMAIL_HOST = config("EMAIL_HOST", cast=str)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = True


# drf-spectacular settings
SPECTACULAR_SETTINGS["SERVERS"] = [
    {
        "url": f"https://{config('SERVER_HOST', cast=str)}/",
        "description": "FL0 Server",
    }
]
