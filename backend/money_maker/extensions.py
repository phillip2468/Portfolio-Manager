from celery import Celery
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

celery = Celery()
db = SQLAlchemy(engine_options={
    "executemany_mode": 'values',
    "executemany_values_page_size": 10000,
    "executemany_batch_page_size": 500
})
migrate = Migrate()

