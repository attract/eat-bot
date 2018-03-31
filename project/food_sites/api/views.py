from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from food_sites.api.serializers import FoodWebsiteSerializer
from ..models import FoodWebsite, FoodProduct


class FoodWebsiteView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = FoodWebsiteSerializer
    queryset = FoodWebsite.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    permission_classes = ()
    filter_fields = ('id', 'product_website__category', )
    ordering_fields = '__all__'

    def get_queryset(self):
        return FoodWebsite.objects.prefetch_related("product_website").all()
