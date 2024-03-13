from .base import *
from settings.constans import Environments


if config("ENVIRONMENT_STATUS") == Environments.TEST.value:

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []

    # Database
    # https://docs.djangoproject.com/en/4.2/ref/settings/#databases
    DATABASES = {}

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.2/howto/static-files/
    STATIC_URL = "static/"
