#!/bin/sh
set -eu

python manage.py migrate --noinput

exec gunicorn daves_music_store.wsgi:application --bind 0.0.0.0:80
