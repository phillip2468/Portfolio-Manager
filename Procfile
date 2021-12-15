web: gunicorn backend.run:app
worker: celery -A backend.money_maker.worker:celery worker -l info -P gevent