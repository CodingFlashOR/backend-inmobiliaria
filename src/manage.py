#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from decouple import config

import os
import sys

from settings.constans import Environments


def set_django_settings_module() -> None:
    """Set DJANGO_SETTINGS_MODULE based on the environment status."""

    environment_status = config("ENVIRONMENT_STATUS", cast=str)

    settings_modules = {
        Environments.DEVELOPMENT.value: "settings.environments.local",
        Environments.PRODUCTION.value: "settings.environments.production",
    }

    try:
        settings_module = settings_modules[environment_status]
    except KeyError:
        raise ValueError(f"Invalid environment status: {environment_status}")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)


def main() -> None:
    """Run administrative tasks."""

    set_django_settings_module()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
