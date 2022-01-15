import os

from celery import Celery
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(engine_options={
    "executemany_mode": 'values',
    "executemany_values_page_size": 10000,
    "executemany_batch_page_size": 500
})
migrate = Migrate()
celery = Celery()
cache = Cache(config={"CACHE_TYPE": "RedisCache",
                      "CACHE_REDIS_URL": os.getenv("REDISCLOUD_URL"),
                      "CACHE_REDIS_DB": "0",})
