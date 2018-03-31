#FROM debian:latest
FROM node:6.7.0

MAINTAINER AttractGroup

RUN apt-get update && apt-get install -y nginx nginx-extras curl git mc
#RUN curl -sL https://deb.nodesource.com/setup_7.x | bash -
#RUN apt-get install -y nodejs
RUN npm install -g bower && npm install -g gulp

ARG project_env
# nginx conf
ADD ./docker/nginx/$project_env/django.conf /etc/nginx/sites-enabled/default

COPY ./project /app

WORKDIR /app/front

#ARG NPM_INSTALL=false
#RUN if [ ${NPM_INSTALL} = true ]; then \
#    npm install && ./node_modules/.bin/gulp prod \
#;fi

COPY ./docker/nginx/entrypoint.sh /entrypoint.sh

RUN sed -i 's/\r//' /entrypoint.sh \
    && chmod +x /entrypoint.sh

EXPOSE 80 443

CMD ["/entrypoint.sh"]