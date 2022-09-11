FROM python:3.10-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/pulp_science
COPY requirements.txt start-server.sh /opt/app/
#COPY .pip_cache /opt/app/pip_cache/
COPY pulp_science /opt/app/pulp_science/
WORKDIR /opt/app
#RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN pip install -r requirements.txt
RUN chown -R www-data:www-data /opt/app

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]
