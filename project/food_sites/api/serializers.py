from rest_framework import serializers

from core.bl.utils_helper import prn
from ..models import FoodWebsite, FoodProduct


class FoodProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodProduct
        fields = '__all__'


class FoodWebsiteSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    # categories = serializers.SerializerMethodField()

    class Meta:
        model = FoodWebsite
        fields = '__all__'

    def get_products(self, obj):
        product_website__category = self.context['request'].GET.get('product_website__category', None)

        product_website = obj.product_website
        if product_website__category:
            product_website = obj.product_website.filter(category=product_website__category)

        serializer = FoodProductSerializer(instance=product_website, many=True)
        return serializer.data

    # def get_categories(self, obj):
    #
    #     return serializer.data