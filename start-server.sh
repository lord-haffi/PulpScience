#!/usr/bin/env bash

# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd pulp_science; python manage.py createsuperuser --no-input)
fi
(cd pulp_science; gunicorn pulp_science.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"
# Gunicorn recommends the number of workers to be set at (2 x $num_cores) + 1.
# You can read more on configuration of Gunicorn here: http://docs.gunicorn.org/en/stable/design.html
