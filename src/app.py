from celery import Celery
from celery import Task
from flask import Flask
from flask import render_template


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="pyamqp://celery:123@rabbitmq/",
            result_backend="redis://redis",
            # task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)

    @app.route("/")
    def index():
        return {"status": "OK"}

    return app


def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app