from __future__ import absolute_import

from celery import Celery, Task
from flask import Flask
from flask_cors import CORS


def create_worker_app():
    app = Flask(__name__)
    CORS(app)

    return app


def init_celery(app):
    new_celery = Celery(include=['backend.money_maker.celery_tasks.tasks'])
    new_celery.conf.broker_url = 'redis://:p16bd01a8b5016a315d6b23b64c53f2eb0813ee6f724f14643f317d6e1d9fc9e3@ec2-34-196-91-164.compute-1.amazonaws.com:6779'
    new_celery.conf.result_backend = 'redis://:p16bd01a8b5016a315d6b23b64c53f2eb0813ee6f724f14643f317d6e1d9fc9e3@ec2-34-196-91-164.compute-1.amazonaws.com:6779'
    new_celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return new_celery


flask_app = create_worker_app()
celery = init_celery(flask_app)
