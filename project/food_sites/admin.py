from django.contrib import admin

from food_sites.models import FoodWebsite, FoodProduct


@admin.register(FoodWebsite)
class FoodWebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']


@admin.register(FoodProduct)
class FoodProductAdmin(admin.ModelAdmin):
    list_display = ['food_website__name', 'image_url', 'name', 'weight', 'price', ]
    search_fields = ['name']
    list_filter = ['food_website']

    def food_website__name(self, obj):
        return obj.food_website.name

    food_website__name.short_description = 'Сайт'

    def image_url(self, obj):
        if obj.image == '/api/nofoto.png':
            obj.image = 'https://kushat.com.ua/api/nofoto.png'
            obj.save()
        return '<img src="%s" width="100">' % obj.image

    image_url.short_description = 'Фото'
    image_url.allow_tags = True
