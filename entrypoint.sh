#!/bin/sh

sleep 5

python manage.py migrate app
python manage.py migrate

rm -rf static
python manage.py collectstatic

python manage.py runserver 0.0.0.0:8000
#gunicorn p2p_project.wsgi:application --bind 0.0.0.0:8000