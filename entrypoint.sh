#!/bin/bash

python manage.py collectstatic --no-input --clear

gunicorn geekshop.wsgi:application -b 0.0.0.0:9999 --reload
