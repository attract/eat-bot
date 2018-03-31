import os
from .common import Common
from configurations import values
try:
    # Python 2.x
    import urlparse
except ImportError:
    # Python 3.x
    from urllib import parse as urlparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):

    # DEBUG = values.BooleanValue(False)

    # for config in Common.TEMPLATES:
    #     config['OPTIONS']['debug'] = DEBUG

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_nose',
                       'rest_framework_swagger',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        BASE_DIR,
        '--nologcapture',
        '--with-coverage',
        '--with-progressive',
        '--cover-package={}'.format(BASE_DIR)
    ]
    
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    #     }
    # }
    redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://eatbot_redis:6379'))
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
    # SUIT_CONFIG = {
    #     'ADMIN_NAME': 'Curbside',
    #     'LIST_PER_PAGE': 20,
    #     'MENU': (
    #         {'app': 'profiles', 'label': 'Profile', 'icon': 'icon-th-list'},
    #         {'app': 'company', 'label': 'Company', 'icon': 'icon-th-list'},
    #         {'app': 'buildings', 'label': 'Building', 'icon': 'icon-th-list'},
    #         {'app': 'food_trucks', 'label': 'Food Truck', 'models': ('foodtruck',), 'icon': 'icon-th'},
    #         {'app': 'events', 'label': 'Events', 'icon': 'icon-th-list'},
    #         {'app': 'schedules', 'label': 'Event schedules', 'models': ('schedule',), 'icon': 'icon-th'},
    #         {'app': 'users', 'label': 'Users', 'icon': 'icon-user', 'models': ('BuildingManager', 'CompanyUserAdmin',
    #                                                                            'Customer', 'FoodTruckAdmin', 'User')},
    #         # {'app': 'files', 'label': 'Files'},
    #         '-',
    #         {'app': 'auth', 'label': 'User group permissions', 'models': ('group', 'permission',), 'icon': 'icon-cog'},
    #         'authtoken',
    #         'sites',
    #         '-',
    #     )
    # }
    # TODO: Configure Redis container in docker to use it for cache

    @property
    def TEMPLATES(self):
        # Remove template caching
        TEMPLATES = Common.TEMPLATES
        TEMPLATES[0]['OPTIONS']['loaders'] = ['django.template.loaders.filesystem.Loader',
                                              'django.template.loaders.app_directories.Loader']
        return TEMPLATES

    # Django RQ local settings
    # RQ_QUEUES = {
    #     'default': {
    #         'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'),
    #         'DB': 0,
    #         'DEFAULT_TIMEOUT': 500,
    #     },
    # }
