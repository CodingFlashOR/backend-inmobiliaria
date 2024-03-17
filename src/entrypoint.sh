#!/bin/sh

echo "Running collectstatic..."
python3 manage.py collectstatic --no-input --settings=settings.environments.production

echo "Running migrations..."
python3 manage.py migrate --settings=settings.environments.production

echo "Starting server..."
gunicorn --env DJANGO_SETTINGS_MODULE=settings.environments.production settings.wsgi:application --bind 0.0.0.0:8000