web: gunicorn --chdir ./backend run:app
worker: cd backend && celery -A money_maker.worker:celery worker