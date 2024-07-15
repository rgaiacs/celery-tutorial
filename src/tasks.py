from celery import Celery

app = Celery("tasks", backend="redis://redis", broker="pyamqp://celery:123@rabbitmq//")


@app.task
def add(x, y):
    return x + y
