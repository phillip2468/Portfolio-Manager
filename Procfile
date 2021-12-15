web: gunicorn --chdir ./backend run:app
worker: celery -A backend.money_maker.worker:celery worker