import os
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from food_sites.models import FoodWebsite, FoodProduct
import subprocess

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour="*/3", minute="0", day_of_week="*")))
def foodwebsite_task():
    """
    :return:
    """
    logger.info("Start `challenge_finish_task` task")
    food_websites = FoodWebsite.objects.all()

    shell_str = 'scrapy crawl food_spider -a id={id_food_website} -a do_action=yes'
    for food_website in food_websites:
        os.system(shell_str.format(id_food_website=food_website.id))

    logger.info("Task `challenge_finish_task` finished")

#
# @periodic_task(run_every=(crontab(hour="0", minute="10", day_of_week="*")))
# def init_week_challenge_task():
#     """
#     Send notifications for customers about day events in area by radius
#     :return:
#     """
#     logger.info("Start `init_week_challenge` task")
#     logger.info("Task `init_week_challenge` finished")

