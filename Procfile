web: gunicorn --chdir ./backend/money_maker wsgi:app
worker: cd backend && celery -A money_maker.celery_app:app worker -l info -P gevent -E