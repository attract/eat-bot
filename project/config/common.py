import os
from configurations import Configuration, values
import environ
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.abspath(os.path.join(os.path.split(__file__)[0], '..'))
path = lambda *args: os.path.join(PROJECT_PATH, *args)

environ.Env().read_env()
env = environ.Env()


class Common(Configuration):

    INSTALLED_APPS = (

        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django.contrib.gis',
        'django.forms',

        'suit',
        'suit_redactor',
        'admin_view_permission',
        'django.contrib.admin',

        # Third party apps
        'corsheaders',
        'django_twilio',
        'rest_framework',  # utilities for rest apis
        'rest_framework.authtoken',  # token authentication
        'rest_auth',
        'rest_auth.registration',
        'django_filters',

        'sorl.thumbnail',
        'expander',  # serialize fields expander

        # Your apps
        'core',
        'authentication',
        'users',
        #'mailer',
    )

    # https://docs.djangoproject.com/en/1.8/topics/http/middleware/
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'core.middleware.MobileDetectionMiddleware',
    )

    USE_SSL = os.getenv("USE_SSL", False)

    if USE_SSL:
        MIDDLEWARE_CLASSES += ('django.middleware.security.SecurityMiddleware',)
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
        SECURE_SSL_REDIRECT = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True

    ROOT_URLCONF = 'urls'
    SECRET_KEY = 'Not a secret'
    WSGI_APPLICATION = 'wsgi.application'

    ALLOWED_HOSTS = ["*"]

    ADMINS = (
        ('Author', 'megajoe1717@gmail.com'),
    )
    BOSS_EMAIL = ADMINS[0][1]
    # Postgres
    # DATABASES = values.DatabaseURLValue('postgres://localhost/furniture_crm')
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': os.environ['POSTGRES_DB'],
            'USER': os.environ['POSTGRES_USER'],
            'PASSWORD': os.environ['POSTGRES_PASSWORD'],
            'HOST': os.environ['POSTGRES_HOST'],
            'PORT': os.environ['POSTGRES_PORT'],
        }
    }

    # Mail Gmail connect
    EMAIL_HOST = env('EMAIL_HOST', default='')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
    EMAIL_PORT = env('EMAIL_PORT', default='587')
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    # taken from https://github.com/pinax/django-mailer
    # TODO USE THIS  WITH CELERY
    # EMAIL_BACKEND = "mailer.backend.DbBackend"

    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = BOSS_EMAIL

    APPEND_SLASH = True
    LOCALE_PATHS = [PROJECT_PATH + '/locale']
    TIME_ZONE = 'America/New_York'
    LANGUAGE_CODE = 'en'

    TIME_INPUT_FORMATS = ('%I:%M%p',)

    # DATETIME_FORMAT = '%Y-%m-%dT%I:%M:%S%z'
    TIME_FORMAT = 'P' # 12 hour format
    DATE_FORMAT_DISPLAY = "%b. %d, %Y"
    USE_I18N = True
    USE_L10N = False
    USE_TZ = True
    # LOGIN_REDIRECT_URL = '/'
    PROTOCOL_FOR_ABSOLUTE_URL = "http"
    SITE_ID = 1

    SERVER_TYPE = os.environ['SERVER_TYPE']
    SITE_DOMAIN = os.environ['SITE_DOMAIN']
    SITE_PROTOCOL = os.environ['SITE_PROTOCOL']
    SITE_URL = '%s://%s' % (SITE_PROTOCOL, SITE_DOMAIN)

     # Media files
    # MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'media')
    # MEDIA_URL = '/media/'
    FIXTURE_DIRS = ['fixtures']

    MEDIA_URL = '/media/'
    MEDIA_ROOT = path('media')

    # Static Files
    # STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')
    # STATICFILES_DIRS = [join(os.path.dirname(BASE_DIR), 'static'),
    # STATICFILES_DIRS = [MEDIA_ROOT + '/sitemaps/', ]

    STATIC_URL = '/static/'
    STATIC_ROOT = path('static')

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            # 'DIRS': [STATICFILES_DIRS],
            'DIRS': [
                str(path('templates')),
            ],
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    'sekizai.context_processors.sekizai',
                ],
                'loaders':[
                    ('django.template.loaders.cached.Loader', [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ]),
                ],
            },
        },
    ]

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    # DEBUG = values.BooleanValue(False)
    # for config in TEMPLATES:
    #     config['OPTIONS']['debug'] = DEBUG
    DEBUG = os.getenv('DEBUG', False)

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'django.server': {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[%(server_time)s] %(message)s',
            },
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'django.server': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'django.server',
            },
            'console': {
                'level': 'INFO',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'verbose',
                'filename': "%s/django.log" % path('logs'),
                'maxBytes': 1024000,
                'backupCount': 3,
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'propagate': True,
            },
            'django.server': {
                'handlers': ['django.server'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['mail_admins', 'file'],
                'level': 'ERROR',
                'propagate': False,
            },

        }
    }

    # Custom user app
    AUTH_USER_MODEL = 'users.User'
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 6,
            }
        },
    ]

    # FOR social_django AUTH

    AUTHENTICATION_BACKENDS = (
        'authentication.backend.AuthBackendBlock',
    )

    # nastya app
    SOCIAL_AUTH_FACEBOOK_KEY = '207451146479699'
    SOCIAL_AUTH_FACEBOOK_SECRET = 'dfde54e0b87397e62bca55a07c85f9d6'

    # nastya app
    SOCIAL_AUTH_TWITTER_KEY = 'HuPOHU5CDuL6oRjL8xFg2JWI5'
    SOCIAL_AUTH_TWITTER_SECRET = '3QhReCvafDfjrsm4MMhp1MOX1QGNlVTxdq4j5c3BRqmbgpV7dH'

    # nastya app
    SOCIAL_AUTH_PINTEREST_KEY = '4943004001334477328'
    SOCIAL_AUTH_PINTEREST_SECRET = '37cc2331cc368e95b3b8c49440a39a550b5949c008e426829712b0ea1ac51ae1'

    FACEBOOK_API_URL = 'https://graph.facebook.com/'
    FACEBOOK_USER_URL = FACEBOOK_API_URL + '%s/?fields=%s&access_token=%s'
    FACEBOOK_PROVIDER = 'facebook'
    TWITTER_API_URL = 'https://api.twitter.com/1.1/account/verify_credentials.json' \
                      '?include_email=true&skip_status=true'  # &include_entities=false'
    TWITTER_PROVIDER = 'twitter'
    PINTEREST_PROVIDER = 'pinterest'
    PINTEREST_API_URL = 'https://api.pinterest.com/v1/me/?access_token=%s'
    SOCIAL_PROVIDER = (
        (FACEBOOK_PROVIDER, 'Facebook'),
        (TWITTER_PROVIDER, 'Twitter'),
        (PINTEREST_PROVIDER, 'Pinterest')
    )

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
        'social_core.pipeline.social_auth.associate_by_email',
    )
    SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'email']

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 20)),
        #'DATETIME_FORMAT': '%Y-%m-%dT%I:%M:%S%z',
        'DATETIME_FORMAT': '%s', #'%s.%f',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'authentication.permissions.IsAuthenticatedCore',
            'authentication.permissions.UserRequestPermission'
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',
                                    'rest_framework.filters.OrderingFilter'),
        'EXCEPTION_HANDLER': 'core.custom_exception.custom_exception_handler',
        'NON_FIELD_ERRORS_KEY': 'non_field_errors',
    }

    # django-rq
    # Adds dashboard link for queues in /admin, This will override the default
    # admin template so it may interfere with other apps that modify the
    # default admin template. If you're using such an app, simply remove this.
    # RQ_SHOW_ADMIN_LINK = True

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True

    # PUSH_NOTIFICATIONS_SETTINGS CONFIGURATION
    PUSH_NOTIFICATIONS_SETTINGS = {
        # "GCM_API_KEY": os.getenv('GOOGLE_API_KEY'),
        # "APNS_CERTIFICATE": str(path(os.getenv('APNS_CERTIFICATE_PATH', default=''))),
        # "APNS_HOST": os.getenv('APNS_HOST', default=''),

        "CONFIG": "push_notifications.conf.AppConfig",
        "APPLICATIONS": {
            # "android_sandbox": {
            #     "PLATFORM": "FCM",
            #     "API_KEY": os.getenv('GOOGLE_API_KEY'),
            # },
            # "android_live": {
            #     "PLATFORM": "FCM",
            #     "API_KEY": os.getenv('GOOGLE_API_KEY'),
            # },
            "fcm": {
                "PLATFORM": "FCM",
                "API_KEY": "AAAArbf5Q1Y:APA91bEhvglWmjIavMftfwQZYhFeqPHq1Cvpd6z0J7y_gEyLxGLvnJ2gLbyzcHRL50ngIUgk2YhbO0KWbQBS0Y_XYgUXWkQfGrJWjtG3bFpFmfbwMt-jt14OYc8gn8KD6EvmNpK79Nht",
            },
            # "ios_sandbox": {
            #     "PLATFORM": "APNS",
            #     "CERTIFICATE": str(path('media_private/push_apns_certs/apns.p8')),
            #     # "HOST": 'gateway.sandbox.push.apple.com',
            #     "USE_SANDBOX": True,
            #     "TOPIC": 'com.fpoc.ios.app'
            # },
            # "ios_live": {
            #     "PLATFORM": "APNS",
            #     "CERTIFICATE": str(path('media_private/push_apns_certs/apns.p8')),
            #     # "HOST": 'gateway.push.apple.com',
            #     "USE_SANDBOX": True,
            #     "TOPIC": 'com.fpoc.ios.app'
            # },
        }
    }

    # PUSH notifications
    PUSH_NOTIFICATIONS_MESSAGES = {
        'CREATE_PHOTO_COMMENT': {
            'type': 'CREATE_PHOTO_COMMENT',
            'title': 'You have a new comment!',
            'msg': _('Check it out!')
        },
        'PHOTO_WINS_COMPETITION': {
            'type': 'PHOTO_WINS_COMPETITION',
            'title': 'Congratulations!',
            'msg': _('Your photo won the competition.')
        },
    }

    # SMS
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', default='')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', default='')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', default='')

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(BASE_DIR,  'media/cache'),
            'TIMEOUT': 60,
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }
    # Social Accounts
    # Facebook configuration
    # SOCIAL_AUTH_FACEBOOK_KEY = '1363142860375563'
    # SOCIAL_AUTH_FACEBOOK_SECRET = 'e64676c57c914e91c5fa404e836b6723'
    #
    # # Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook.
    # # Email is not sent by default, to get it, you must request the email permission:
    # SOCIAL_AUTH_FACEBOOK_SCOPE = ['phone']
    # SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    #     'fields': 'name, email'
    # }
    # PROPRIETARY_BACKEND_NAME = 'Facebook'

    # ACCOUNT_USER_MODEL_USERNAME_FIELD = 'phone'
    # ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
    # ACCOUNT_EMAIL_VERIFICATION = 'none'
    # SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
    # SOCIALACCOUNT_EMAIL_REQUIRED = False
    # SOCIALACCOUNT_QUERY_EMAIL = True

    # PHONENUMBER_DB_FORMAT = 'RFC3966'
    # PHONENUMBER_DEFAULT_REGION = 'US'

    # Django Suit
    # http://getbootstrap.com/2.3.2/base-css.html#icons
    # https://github.com/darklow/django-suit/tree/develop/suit/templates

    SUIT_CONFIG = {
        'ADMIN_NAME': 'Pet Rater',
        'SEARCH_URL': '',
        'LIST_PER_PAGE': 20,
        'CONFIRM_UNSAVED_CHANGES': False,
        'MENU': (
            {'app': 'users', 'label': 'Users', 'icon': 'icon-user', 'permissions': ['users.add_user'], },
            {'app': 'categories', 'label': 'Categories', 'icon': 'icon-th-list', 'permissions': ['category.add_category'], },
            {'app': 'photos', 'label': 'Photos', 'icon': 'icon-camera', },
            {'app': 'reports', 'label': 'Reports', 'icon': 'icon-info-sign', },
            {'app': 'pages', 'label': 'Pages', 'icon': 'icon-list-alt', },
            {'app': 'ranking', 'label': 'Ranking', 'icon': 'icon-star-empty', },
            {'app': 'notifications', 'label': 'Notifications', 'icon': 'icon-info-sign', },
        )
    }

    FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
    DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

    TEMPLATE_DEBUG = False

    THUMBNAIL_DEBUG = True
    THUMBNAIL_DUMMY = True
    THUMBNAIL_FORMAT = 'PNG'  # With format JPG got exception "cannot write mode RGBA as JPEG"
    THUMBNAIL_BACKEND = 'core.bl.thumbnail_engine.DummyThumbnailBackend'
    THUMBNAIL_DUMMY_SOURCE = '/media/img/no-img.jpg'
    # THUMBNAIL_DUMMY_SOURCE_SMALL = '/media/img/no-img-sm.png'
    THUMBNAIL_URL_TIMEOUT = 2
