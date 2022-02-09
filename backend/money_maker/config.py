import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("DATABASE_URL")
if uri is not None and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = True
ENV = "development"
CELERY = {
    "broker_url": os.getenv("REDIS_URL"),
    "result_backend": os.getenv("REDIS_URL"),
    "result_serializer": 'json'
}

SQLALCHEMY_ENGINE_OPTIONS = {
    "executemany_mode": 'values',
    "executemany_values_page_size": 10000,
    "executemany_batch_page_size": 500,
}
SECRET_KEY = os.getenv("SECRET_KEY")

JWT_COOKIE_SECURE = True
JWT_TOKEN_LOCATION = ["cookies"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
JWT_COOKIE_CSRF_PROTECT = True
JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN-REFRESH"
JWT_CSRF_IN_COOKIES = False
