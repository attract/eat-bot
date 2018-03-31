from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour="0", minute="0", day_of_week="*")))
def challenge_finish_task():
    """
    Define photo winners in each challenge at prev week
    :return:
    """
    logger.info("Start `challenge_finish_task` task")
    logger.info("Task `challenge_finish_task` finished")


@periodic_task(run_every=(crontab(hour="0", minute="10", day_of_week="*")))
def init_week_challenge_task():
    """
    Send notifications for customers about day events in area by radius
    :return:
    """
    logger.info("Start `init_week_challenge` task")
    logger.info("Task `init_week_challenge` finished")
