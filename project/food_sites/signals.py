from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from core.bl.point import get_point

from core.bl.utils_helper import prn
from core.utils import EmailNotification
from food_sites.models import FoodProduct


@receiver(pre_save, sender=FoodProduct)
def product_post_save_signal(sender, instance=None, created=False, **kwargs):
    instance.is_hidden = False
