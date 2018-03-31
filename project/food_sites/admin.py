from django.contrib import admin

from food_sites.models import FoodWebsite, FoodProduct


@admin.register(FoodWebsite)
class FoodWebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']


@admin.register(FoodProduct)
class FoodProductAdmin(admin.ModelAdmin):
    list_display = ['food_website__name', 'image_url', 'name', 'category', 'description_html',
                    'weight', 'price', ]
    search_fields = ['name', 'category', ]
    list_filter = ['food_website', 'category', ]

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

    def description_html(self, obj):
        return obj.description

    description_html.short_description = 'Описание'
    description_html.allow_tags = True
