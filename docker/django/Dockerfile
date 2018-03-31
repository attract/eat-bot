FROM python:3.5
ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./docker/django/req.txt /requirements/req.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements/req.txt

RUN apt-get update -y \
    && apt-get install -y gettext
    #&& apt-get install -y cron

# Install postgres requirements
RUN apt-get install -y \
    postgresql-server-dev-all \
    libgeos-dev \
    libgdal-dev \
    postgresql-client

ENV TZ=America/Tijuana

COPY ./project /app

COPY ./docker/django/gunicorn.sh /gunicorn.sh
COPY ./docker/django/entrypoint.sh /django/entrypoint.sh

RUN sed -i 's/\r//' /django/entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /django/entrypoint.sh \
    && chmod +x /gunicorn.sh

WORKDIR /app

EXPOSE 8000 5555 5000

ENTRYPOINT ["/django/entrypoint.sh"]
