from django.db import models
from rest_framework.serializers import ModelSerializer

from core.fields import TimestampField


class ModelSerializerCore(ModelSerializer):

    ModelSerializer.serializer_field_mapping[models.DateTimeField] = TimestampField
