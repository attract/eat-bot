from __future__ import unicode_literals
from dynamic_scraper.spiders.django_spider import DjangoSpider

from core.bl.utils_helper import prn
from food_sites.models import FoodProduct, FoodWebsite, FoodProductItem


class FoodSpider(DjangoSpider):
    name = 'food_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(FoodWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = FoodProduct
        self.scraped_obj_item_class = FoodProductItem

        # Set all products hiddes
        self.ref_object.product_website.update(is_hidden=True)
        try:
            super(FoodSpider, self).__init__(self, *args, **kwargs)
        except Exception as ex:
            prn(ex)
