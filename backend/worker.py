from os import environ

from celery import Celery
from backend.money_maker import create_worker_app


def init_celery(app):
    celery = Celery()
    celery.conf.broker_url = environ.get('CELERY_BROKER_URL')
    # celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = create_worker_app()
celery = init_celery(flask_app)

