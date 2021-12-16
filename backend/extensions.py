from celery import Celery

celery = Celery()


def register_extensions(app, worker=False):
    celery.config_from_object(app.config)

    if not worker:
        pass
