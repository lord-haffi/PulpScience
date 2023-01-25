#!/usr/bin/env bash

# start-server.sh
python manage.py migrate
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    python manage.py createsuperuser --no-input
fi
(gunicorn pulp_science.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"
# Gunicorn recommends the number of workers to be set at (2 x $num_cores) + 1.
# You can read more on configuration of Gunicorn here: http://docs.gunicorn.org/en/stable/design.html
