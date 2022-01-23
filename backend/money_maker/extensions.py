import os
from urllib.parse import urlparse

from celery import Celery
from dotenv import load_dotenv
from flask_caching import Cache
from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_praetorian import Praetorian
from flask_cors import CORS

load_dotenv()

db = SQLAlchemy(engine_options={
    "executemany_mode": 'values',
    "executemany_values_page_size": 10000,
    "executemany_batch_page_size": 500
})
celery = Celery()
url = urlparse(os.getenv("REDISCLOUD_URL"))
cache = Cache(config={"CACHE_TYPE": "RedisCache",
                      "CACHE_REDIS_HOST": url.hostname,
                      "CACHE_REDIS_PORT": url.port,
                      "CACHE_REDIS_DB": "0",
                      "CACHE_REDIS_PASSWORD": url.password})
csrf = SeaSurf()
talisman = Talisman()
praetorian = Praetorian()
cors = CORS()
