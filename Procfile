web: gunicorn --chdir ./backend run:app
worker: cd backend && celery -A money_maker.celery_app:app worker -l info -P gevent -E