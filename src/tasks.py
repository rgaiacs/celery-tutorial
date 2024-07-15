import time

from celery import shared_task


@shared_task(ignore_result=False)
def add(a, b):
    return a + b