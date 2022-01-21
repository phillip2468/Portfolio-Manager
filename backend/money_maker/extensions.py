import os
from urllib.parse import urlparse

from celery import Celery
from dotenv import load_dotenv
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_seasurf import SeaSurf
from flask_talisman import Talisman
from flask_dramatiq import Dramatiq
from periodiq import PeriodiqMiddleware

load_dotenv()

db = SQLAlchemy(engine_options={
    "executemany_mode": 'values',
    "executemany_values_page_size": 10000,
    "executemany_batch_page_size": 500
})
migrate = Migrate()
celery = Celery()
url = urlparse(os.getenv("REDISCLOUD_URL"))
cache = Cache(config={"CACHE_TYPE": "RedisCache",
                      "CACHE_REDIS_HOST": url.hostname,
                      "CACHE_REDIS_PORT": url.port,
                      "CACHE_REDIS_DB": "0",
                      "CACHE_REDIS_PASSWORD": url.password})
csrf = SeaSurf()
talisman = Talisman()
dramatiq = Dramatiq()
dramatiq.middleware.append(PeriodiqMiddleware())
