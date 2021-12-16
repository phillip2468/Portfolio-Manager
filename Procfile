web: gunicorn --chdir ./backend run:app
cd backend
worker: celery -A backend.money_maker.worker:celery worker