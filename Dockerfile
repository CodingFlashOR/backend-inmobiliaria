FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip

COPY ./src ./

RUN pip install -r requirements.txt

CMD [ "sh", "entrypoint.sh" ]