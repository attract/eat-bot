from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.bl.utils_helper import prn
from food_sites.models import FoodProduct
from lxml import html
from lxml import etree


@receiver(pre_save, sender=FoodProduct)
def product_pre_save_signal(sender, instance=None, created=False, **kwargs):
    instance.is_hidden = False
    # ONLY FOR kushat podano
    if '<table>' in instance.description:
        parsed_body = html.fromstring(instance.description)
        all_tr = parsed_body.xpath('.//tr')
        count_all_tr = len(all_tr)
        prn(count_all_tr)
        cur_tr = 0
        description_fixed = '<table><tbody>'
        for one_tr in parsed_body.xpath('.//tr'):
            cur_tr += 1
            prn(one_tr)
            tr_html = etree.tostring(one_tr, pretty_print=True).decode("utf-8")
            prn(tr_html)
            if cur_tr < count_all_tr - 4:
                description_fixed += tr_html

        instance.description = description_fixed + '</tbody></table>'

    instance.category = instance.category.strip()
