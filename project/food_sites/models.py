from django.conf import settings
from django.db import models
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem
import scrapy

from core.bl.utils_helper import prn


class FoodWebsite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Web-сайт'
        verbose_name_plural = 'Web-сайты'


class FoodProduct(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    weight = models.CharField(max_length=100, blank=True, default='')
    category = models.CharField(max_length=255, blank=True, default='')
    #image = models.ImageField(verbose_name="Фото", upload_to=settings.IMAGE_PATH, default=None)
    image = models.CharField(max_length=255, blank=True, default='')
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=9, default=0)
    food_website = models.ForeignKey(FoodWebsite, verbose_name="Сайт", related_name="product_website")
    url = models.URLField()
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    is_hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


# def image_serializer(value):
#     prn('https://kushat.com.ua/%s' % str(value))
#     return 'https://kushat.com.ua/%s' % str(value)


class FoodProductItem(DjangoItem):
    django_model = FoodProduct
    # image = scrapy.Field(FoodProduct.fields['name'], serializer=image_serializer)

    # def save(self, commit=True):
    #
    #     prn(self)
    #     if commit:
    #         self.instance.save()
    #     return self.instance


