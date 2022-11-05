FROM python:3.10.6-alpine3.15

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/MagicHelper

RUN addgroup -S MagicHelper && adduser -S MagicHelper -G MagicHelper

ENV PROJECT_HOME=/home/MagicHelper/vk_webhook
RUN mkdir -p ${PROJECT_HOME}
WORKDIR ${PROJECT_HOME}

COPY ./docker/ ./docker/
COPY ./app/ ./app/
COPY ./poetry.lock .
COPY ./pyproject.toml .

RUN chmod +x ${PROJECT_HOME}/docker/webhook/entrypoint.sh

RUN apk update
RUN apk add postgresql-dev gcc libpq libpq-dev python3-dev musl-dev libffi-dev openssl-dev cargo libxml2-dev libxslt-dev tzdata
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir poetry
RUN python -m poetry config virtualenvs.create false
RUN python -m poetry install --no-dev
RUN apk del cargo 

RUN chown -R MagicHelper:MagicHelper ${PROJECT_HOME}

USER MagicHelper

ENTRYPOINT ["/bin/sh", "/home/MagicHelper/vk_webhook/docker/webhook/entrypoint.sh"]
