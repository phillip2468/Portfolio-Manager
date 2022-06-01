web: gunicorn --chdir ./backend run:app
worker: cd backend && celery -A money_maker.celery_app:app worker -l error --concurrency=2 -E --beat
