FROM python:3.11.5-alpine3.17

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk add --no-cache \
  gcc \
  musl-dev \
  postgresql-dev \
  python3-dev \
  libffi-dev

COPY ./src ./

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

CMD [ "sh", "-c", "python manage.py migrate --settings=settings.environments.production && \
    python manage.py collectstatic --noinput --clear --settings=settings.environments.production && \
    gunicorn settings.wsgi:application --env DJANGO_SETTINGS_MODULE=settings.environments.production" ]