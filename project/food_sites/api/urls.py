from rest_framework import routers

from .views import FoodWebsiteView

router = routers.SimpleRouter()

router.register(r'foodwebsite', FoodWebsiteView, base_name='foodwebsite')

urlpatterns = [
]

urlpatterns += router.urls
