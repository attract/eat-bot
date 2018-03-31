import os
from configurations import values
# from boto.s3.connection import OrdinaryCallingFormat
from .common import Common

try:
    # Python 2.x
    import urlparse
except ImportError:
    # Python 3.x
    from urllib import parse as urlparse


class Production(Common):

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    # SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    DEBUG = os.getenv('DEBUG', False)

    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = values.SecretValue()

    # Site
    # https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts

    INSTALLED_APPS += ("gunicorn", 'rest_framework_swagger',)

    # Template
    # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

    AWS_HEADERS = {
        'Cache-Control': 'max-age=86400, s-maxage=86400, must-revalidate',
    }

    # Static files
    # STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
    # TODO: Configure Redis container in docker to use it
    # Caching
    redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://petrater_redis:6379'))
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '{}:{}'.format(redis_url.hostname, redis_url.port),
            'OPTIONS': {
                'DB': 0,
                'PASSWORD': redis_url.password,
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                'CONNECTION_POOL_CLASS_KWARGS': {
                    'max_connections': 50,
                    'timeout': 20,
                }
            }
        }
    }

    # Django RQ production settings
    # RQ_QUEUES = {
    #     'default': {
    #         'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'),
    #         'DB': 0,
    #         'DEFAULT_TIMEOUT': 500,
    #     },
    # }
