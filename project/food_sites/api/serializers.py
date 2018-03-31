from rest_framework import serializers
from ..models import FoodWebsite, FoodProduct


class FoodWebsiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodWebsite
        exclude = ['point']
        read_only_fields = ('status', 'owner')
