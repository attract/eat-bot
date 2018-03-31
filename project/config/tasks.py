from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from celery.task import task
from django.db.models import Q
from dynamic_scraper.utils.task_utils import TaskUtils
from food_sites.models import FoodWebsite, FoodProduct

logger = get_task_logger(__name__)


# @periodic_task(run_every=(crontab(hour="0", minute="0", day_of_week="*")))
# def challenge_finish_task():
#     """
#     Define photo winners in each challenge at prev week
#     :return:
#     """
#     logger.info("Start `challenge_finish_task` task")
#     logger.info("Task `challenge_finish_task` finished")
#
#
# @periodic_task(run_every=(crontab(hour="0", minute="10", day_of_week="*")))
# def init_week_challenge_task():
#     """
#     Send notifications for customers about day events in area by radius
#     :return:
#     """
#     logger.info("Start `init_week_challenge` task")
#     logger.info("Task `init_week_challenge` finished")

@task()
def run_spiders():
    logger.info("Start `run_spiders` task")

    t = TaskUtils()
    #Optional: Django field lookup keyword arguments to specify which reference objects (NewsWebsite)
    #to use for spider runs, e.g.:
    # kwargs = {
    #     'scrape_me': True,  #imaginary, model NewsWebsite hat no attribute 'scrape_me' in example
    # }
    #Optional as well: For more complex lookups you can pass Q objects vi args argument
    # args = (Q(name='Wikinews'),)
    kwargs = {}
    args = ()
    try:
        t.run_spiders(FoodWebsite, 'scraper', 'scraper_runtime', 'food_spider', *args, **kwargs)
    except Exception as ex:
        print(ex)

    logger.info("Task `run_spiders` finished")


# @task()
# def run_checkers():
#     t = TaskUtils()
#     #Optional: Django field lookup keyword arguments to specify which reference objects (Article)
#     #to use for checker runs, e.g.:
#     kwargs = {
#         'check_me': True, #imaginary, model Article hat no attribute 'check_me' in example
#     }
#     #Optional as well: For more complex lookups you can pass Q objects vi args argument
#     args = (Q(id__gt=100),)
#     t.run_checkers(FoodProduct, 'news_website__scraper', 'checker_runtime', 'article_checker', *args, **kwargs)
