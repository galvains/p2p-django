#!/bin/sh

python manage.py migrate app

rm -rf static
python manage.py collectstatic

gunicorn p2p_project.wsgi:application --bind 0.0.0.0:8000