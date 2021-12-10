FROM python:3.9-slim

ARG DEBUG=False

RUN echo "${DEBUG}" | tr [:upper:] [:lower:] > /tmp/debug

ENV POETRY_VERSION=1.1.12 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_ROOT_WARNING=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

RUN if [ $(cat /tmp/debug) != true ]; then export PYTHONDONTWRITEBYTECODE=1; fi

RUN apt-get update \
    && apt-get install -y nginx git-all libxml2-dev libxslt1-dev libffi-dev build-essential libssl-dev libpq-dev supervisor --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

RUN pip install -U pip
RUN pip install "poetry==${POETRY_VERSION}"

COPY poetry.lock pyproject.toml /app/

RUN poetry install $(test "$(cat /tmp/debug)" != true && echo "--no-dev")

COPY . /app
RUN chmod +x ./app/conf/start.sh

RUN rm -f /etc/nginx/sites-enabled/default
RUN ln -s ./app/conf/nginx /etc/nginx/sites-enabled/default

RUN cp ./app/conf/supervisord.conf /etc/supervisor/conf.d/app.conf

# RUN rm /tmp/debug

RUN python /app/manage.py collectstatic --no-input

EXPOSE 8001

CMD [ "/app/app/conf/start.sh" ]
