from rest_framework import serializers
from ..models import FoodWebsite, FoodProduct


class FoodWebsiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodWebsite
        fields = '__all__'

