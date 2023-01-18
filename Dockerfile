FROM python:3.10-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/PulpScience
COPY requirements.txt start-server.sh /opt/app/
#COPY .pip_cache /opt/app/pip_cache/
COPY PulpScience /opt/app/PulpScience/
COPY homepage /opt/app/homepage/
COPY manage.py /opt/app/manage.py
COPY PulpScience/settings_production.py /opt/app/PulpScience/settings.py
WORKDIR /opt/app
# install psycopg2 for postgresql
RUN apt install python3-psycopg2
#RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN pip install -r requirements.txt
RUN chown -R www-data:www-data /opt/app
# install psycopg2-binary into venv
RUN pip install psycopg2-binary

# Collect static files for production environment
RUN python manage.py collectstatic
# Apply migrations to database
# RUN (cd PulpScience/ && python manage.py migrate)

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]
