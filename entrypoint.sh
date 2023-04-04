#!/bin/bash
APP_PORT=${PORT:-8000}
python manage.py collectstatic
DJANGO_SETTINGS_MODULE=django_regularize.settings DJANGO_CONFIGURATION=Prod gunicorn --worker-tmp-dir /dev/shm django_regularize.wsgi:application --bind "0.0.0.0:${APP_PORT}"