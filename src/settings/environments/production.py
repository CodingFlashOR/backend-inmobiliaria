import os

from .base import *
from settings.constans import Environments


if config("ENVIRONMENT_STATUS") == Environments.PRODUCTION.value:
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = []

    CSRF_TRUSTED_ORIGINS = []

    # Database
    # https://docs.djangoproject.com/en/4.2/ref/settings/#databases
    DATABASES = {}

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.2/howto/static-files/
    STATIC_URL = "static/"

    STATIC_ROOT = os.path.join("app", "static")

    STATICFILES_STORAGE = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )

    # CORS settings
    CORS_ORIGIN_ALLOW_ALL = False

    CORS_ORIGIN_WHITELIST = []
