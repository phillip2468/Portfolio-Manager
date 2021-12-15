web: gunicorn backend.run:app
worker: celery worker -A backend.money_maker.celery_tasks:tasks