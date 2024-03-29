FROM python:3.11-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
WORKDIR /opt/app
RUN chown -R www-data:www-data /opt/app
# install psycopg2 for postgresql
RUN apt install python3-psycopg2
#RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
COPY requirements.txt start-server.sh /opt/app/
RUN pip install -r requirements.txt
# install psycopg2-binary into venv
RUN pip install psycopg2-binary
#COPY .pip_cache /opt/app/pip_cache/
COPY pulp_science /opt/app/pulp_science/
COPY pulp_science/settings_production.py /opt/app/pulp_science/settings.py
COPY homepage /opt/app/homepage/
COPY manage.py /opt/app/manage.py

# Collect static files for production environment
RUN python manage.py collectstatic

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]
