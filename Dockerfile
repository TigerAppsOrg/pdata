# Dockerfile
# pdata
# Author: Rushy Panchal
# Date: December 27th, 2017
# Description: Docker configuration.

FROM python:3.6.4-alpine3.7
LABEL maintainer="Rushy Panchal <rpanchal@princeton.edu>"

ARG APP_DIR="/opt/pdata"
ARG PORT=8080

ENV DOCKER_CONTAINER 1
ENV APP_DIR "$APP_DIR"
ENV PORT "$PORT"

### Dependencies ###
# By copying the Pipfile.lock file before the code, making a change in the
# code does not cause requirements to be reinstalled unless Pipfile.lock
# also changed.
COPY Pipfile "$APP_DIR/Pipfile"
COPY Pipfile.lock "$APP_DIR/Pipfile.lock"

WORKDIR "$APP_DIR"

RUN apk add --no-cache pcre-dev postgresql-dev

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
            gcc \
            make \
            libc-dev \
            musl-dev \
            linux-headers \
    && pip install --no-cache-dir pipenv  \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pipenv install --system" \
    && runDeps="$( \
            scanelf --needed --nobanner --recursive /venv \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps

### Deployment ###
COPY . "$APP_DIR"
EXPOSE "$PORT"
CMD ["uwsgi", "--ini", "uwsgi.ini"]
