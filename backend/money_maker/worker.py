from os import environ

from celery import Celery
from backend.money_maker.app import create_worker_app


def init_celery(app):
    new_celery = Celery()
    new_celery.conf.broker_url = environ.get('CELERY_BROKER_URL')
    # celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    new_celery.conf.update(app.config)
    print('lol')

    class ContextTask(new_celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    new_celery.Task = ContextTask
    return new_celery


flask_app = create_worker_app()
celery = init_celery(flask_app)
