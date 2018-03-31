from __future__ import unicode_literals
from dynamic_scraper.spiders.django_checker import DjangoChecker
from food_sites.models import FoodProduct


class FoodChecker(DjangoChecker):
    name = 'food_checker'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(FoodProduct, **kwargs)
        self.scraper = self.ref_object.food_website.scraper
        # self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.checker_runtime
        super(FoodChecker, self).__init__(self, *args, **kwargs)
