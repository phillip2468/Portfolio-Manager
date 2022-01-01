import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY = {
    "broker_url": os.getenv("REDIS_URL"),
    "result_backend": os.getenv("REDIS_URL"),
    "result_serializer": 'json'
}