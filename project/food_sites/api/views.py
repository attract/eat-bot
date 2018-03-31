from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from food_sites.api.serializers import FoodWebsiteSerializer
from ..models import FoodWebsite, FoodProduct


class FoodWebsiteView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = FoodWebsiteSerializer
    queryset = FoodWebsite.objects.all()

