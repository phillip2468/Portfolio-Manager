from celery import Celery
from flask import Flask

from .home.routes import home_bp
from os import environ


def init_celery(app):
    celery = Celery()
    celery.conf.broker_url = environ.get('CELERY_BROKER_URL')
    #celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    init_celery(app)

    return app
