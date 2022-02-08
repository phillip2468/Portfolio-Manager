import os
from urllib.parse import urlparse

from celery import Celery
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

load_dotenv()

db = SQLAlchemy()
celery = Celery()
url = urlparse(os.getenv("REDISCLOUD_URL"))
cache = Cache(config={"CACHE_TYPE": "RedisCache",
                      "CACHE_REDIS_HOST": url.hostname,
                      "CACHE_REDIS_PORT": url.port,
                      "CACHE_REDIS_DB": "0",
                      "CACHE_REDIS_PASSWORD": url.password})
talisman = Talisman()
cors = CORS()
jwt_manager = JWTManager()
bcrypt = Bcrypt()
marshmallow = Marshmallow()
