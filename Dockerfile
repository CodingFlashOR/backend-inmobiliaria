FROM python:3.11.5-alpine3.17

ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT production

WORKDIR /app

RUN apk add --no-cache \
  gcc \
  musl-dev \
  postgresql-dev \
  python3-dev \
  libffi-dev

RUN pip install --upgrade pip && \
  pip install poetry

COPY ./api_inmobiliaria ./

COPY ./pyproject.toml ./

COPY ./poetry.lock ./

RUN poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-ansi

CMD [ "sh", "-c",
  "python manage.py migrate --settings=settings.environments.$ENVIRONMENT && \
  python manage.py collectstatic --noinput --clear --settings=settings.environments.$ENVIRONMENT && \
  gunicorn settings.wsgi:application --env DJANGO_SETTINGS_MODULE=settings.environments.$ENVIRONMENT" ]
