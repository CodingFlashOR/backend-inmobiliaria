"""
WSGI config for prueba project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from manage import set_django_settings_module


set_django_settings_module()

application = get_wsgi_application()
