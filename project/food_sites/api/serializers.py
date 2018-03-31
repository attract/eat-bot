from django.db.models import Count
from rest_framework import serializers

from core.bl.utils_helper import prn
from ..models import FoodWebsite, FoodProduct


class FoodProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodProduct
        fields = '__all__'


class FoodCategorySerializer(serializers.ModelSerializer):
    qnt = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = FoodProduct
        fields = ['category', 'qnt', 'products']

    def get_qnt(self, obj):
        return obj['qnt']

    def get_products(self, obj):
        serializer = FoodProductSerializer(instance=obj['products'], many=True)
        return serializer.data


class FoodWebsiteSerializer(serializers.ModelSerializer):
    # products = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = FoodWebsite
        fields = '__all__'

    def get_categories(self, obj):
        categories = obj.product_website.values('category',).annotate(qnt=Count('category'))
        product_website__category = self.context['request'].GET.get('product_website__category', None)

        for category in categories:
            category['products'] = []

            category['products'] = obj.product_website.filter(category=category['category'])
            if product_website__category:
                category['products'] = category['products'].filter(category=product_website__category)

        serializer = FoodCategorySerializer(instance=categories, many=True)

        return serializer.data
