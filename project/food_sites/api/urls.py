from rest_framework import routers

from .views import FoodWebsiteView, FoodProductView

router = routers.SimpleRouter()

router.register(r'foodwebsite', FoodWebsiteView, base_name='foodwebsite')
router.register(r'food_product', FoodProductView, base_name='food_product')

urlpatterns = [
]

urlpatterns += router.urls
