#!/bin/bash

set -e

python /app/manage.py migrate

if [[ "$(tr [:upper:] [:lower:] <<< ${DEBUG})" == "true" ]]; then
    python /app/manage.py runserver_plus 0:8000
else
    supervisord -n -c /etc/supervisor/supervisord.conf
fi
