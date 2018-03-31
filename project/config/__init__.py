from __future__ import absolute_import
from .celery import app as celery_app

from .local import Local  # noqa
from .production import Production  # noqa
