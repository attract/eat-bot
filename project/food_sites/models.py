from django.conf import settings
from django.db import models
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem


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
    image = models.ImageField(verbose_name="Фото", upload_to=settings.IMAGE_PATH, default=None)
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, max_digits=9, default=0)
    food_website = models.ForeignKey(FoodWebsite)
    url = models.URLField()
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class FoodProductItem(DjangoItem):
    django_model = FoodProduct



