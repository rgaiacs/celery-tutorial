from celery import Celery

app = Celery('tasks', broker='pyamqp://celery:123@rabbitmq//')

@app.task
def add(x, y):
    return x + y