import dj_database_url

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = [config("CLIENT_HOST"), config("SERVER_HOST")]

CSRF_TRUSTED_ORIGINS = [
    f"https://{config('SERVER_HOST')}",
    f"https://{config('CLIENT_HOST')}",
]

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True


# CORS settings
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [f"https://{config('CLIENT_HOST')}"]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": dj_database_url.config(
        default=config("POSTGRE_DB_URL"),
        engine="django.db.backends.postgresql",
    ),
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
DEFAULT_FROM_EMAIL = config("EMAIL_HOST_USER")
EMAIL_FROM_USER = config("EMAIL_HOST_USER")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = True


# drf-spectacular settings
SPECTACULAR_SETTINGS["SERVERS"] = [
    {"url": f"https://{config('SERVER_HOST')}/", "description": "FL0 Server"}
]
