web: gunicorn backend.run:app
worker: celery worker -A --app=backend.money_maker.celery_tasks.tasks