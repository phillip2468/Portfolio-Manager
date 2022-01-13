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
cache = Cache(config={"CACHE_TYPE": "RedisCache", "CACHE_REDIS_URL": "redis://:p4f59a8e2e5f342d5eba3e0f0c6d7e2248726b02b3ebf626676b67d2982281882@ec2-18-207-70-186.compute-1.amazonaws.com:24039"})