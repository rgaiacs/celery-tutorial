import random
import time

from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task(ignore_result=False)
def add(a, b):
    logger.info("Adding %d + %d" % (a, b))
    time.sleep(random.randint(20, 30))
    return a + b


@task_postrun.connect(sender=add)
def task_postrun_notifier(sender=None, **kwargs):
    print("From task_postrun_notifier ==> Ok, done!")
