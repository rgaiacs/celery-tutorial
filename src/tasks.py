import random
import time

from celery import shared_task
from celery import chain
from celery.signals import task_postrun
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task(ignore_result=False)
def add(a, b):
    logger.info("Scheduling to add %d + %d" % (a, b))
    time.sleep(random.randint(2, 3))
    logger.info("Adding %d + %d" % (a, b))
    return a + b


@task_postrun.connect(sender=add)
def task_add_postrun_notifier(sender=None, **kwargs):
    print("From task_add_postrun_notifier ==> Ok, done!")


@shared_task(ignore_result=False)
def mul(a, b):
    logger.info("Scheduling to multiply %d + %d" % (a, b))
    time.sleep(random.randint(2, 3))
    logger.info("Multiplying %d + %d" % (a, b))
    return a + b


@task_postrun.connect(sender=mul)
def task_mul_postrun_notifier(sender=None, **kwargs):
    print("From task_mul_postrun_notifier ==> Ok, done!")


@shared_task(ignore_result=False)
def square(a):
    logger.info("Scheduling to square %d" % a)
    time.sleep(random.randint(2, 3))
    logger.info("Squaring %d" % a)
    return a * a


@task_postrun.connect(sender=square)
def task_square_postrun_notifier(sender=None, **kwargs):
    print("From task_square_postrun_notifier ==> Ok, done!")


def all(a, b):
    return chain(add.s(a, b), square.s())
