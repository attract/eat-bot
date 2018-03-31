import os

import djcelery

# -- Celery related configuration
djcelery.setup_loader()


class CeleryConfig:
    BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'

    CELERY_RESULT_BACKEND = 'amqp'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_IMPORTS = ('config.tasks', )
