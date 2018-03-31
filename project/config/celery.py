from __future__ import absolute_import

import os

from celery import Celery

"""
Celery with Rebbit.

Starting/Stopping the RabbitMQ server:
$ sudo rabbitmq-server - start
$ sudo rabbitmq-server -detached - start with the background (as a daemon)
$ sudo rabbitmqctl stop

Start celery:
$ celery -A fivel worker -l info
./celeryd.sh

"""

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.local')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

# import configurations
# configurations.setup()

from configurations import importer
importer.install()

from django.conf import settings


app = Celery('config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


