web: cd backend && ./bin/start-nginx gunicorn run:app -p /tmp/app-initialized --log-file - --bind 127.0.0.1:8087
worker: cd backend && celery -A money_maker.celery_app:app worker -l info --concurrency=2 -E --beat
