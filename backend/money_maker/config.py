import os

from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("DATABASE_URL")
if uri is not None and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
ENV = "development"
MEMCACHIER_SERVERS = "mc5.dev.ec2.memcachier.com:11211"
MEMCACHIER_USERNAME = "D51F65"
MEMCACHIER_PASSWORD = "29336A344020CDF655FE6BD85C406D05"

CELERY = {
    "broker_url": os.getenv("REDIS_URL"),
    "result_backend": os.getenv("REDIS_URL"),
    "result_serializer": 'json'
}

SQLALCHEMY_ENGINE_OPTIONS = {
    "executemany_mode": 'values',
    "executemany_values_page_size": 10000
}
