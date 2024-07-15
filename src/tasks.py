import random
import time

from celery import shared_task
from celery.signals import task_postrun


@shared_task(ignore_result=False)
def add(a, b):
    time.sleep(random.randint(5, 30))
    return a + b

@task_postrun.connect(sender=add)
def task_postrun_notifier(sender=None, **kwargs):
    print("From task_postrun_notifier ==> Ok, done!")