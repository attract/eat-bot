from django.contrib import admin

from food_sites.models import FoodWebsite, FoodProduct


@admin.register(FoodWebsite)
class FoodWebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']


@admin.register(FoodProduct)
class FoodProductAdmin(admin.ModelAdmin):
    list_display = ['food_website', 'image', 'name', 'weight', 'price', ]
    list_filter = ['food_website']
