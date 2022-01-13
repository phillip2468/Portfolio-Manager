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
                      "CACHE_REDIS_HOST": "redis-15988.c84.us-east-1-2.ec2.cloud.redislabs.com",
                      "CACHE_REDIS_PORT": "15988",
                      "CACHE_REDIS_DB": "0",
                      "CACHE_REDIS_PASSWORD": "2nVsLWNYq4qeEGU48zDgOQjRLHkk0PcB"})
