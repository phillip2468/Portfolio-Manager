import os

from dotenv import load_dotenv
from dramatiq.brokers.redis import RedisBroker

load_dotenv()

uri = os.getenv("DATABASE_URL")
if uri is not None and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = True
ENV = "development"

SQLALCHEMY_ENGINE_OPTIONS = {
    "executemany_mode": 'values',
    "executemany_values_page_size": 10000
}
SECRET_KEY = os.getenv("SECRET_KEY")
DRAMATIQ_BROKER = RedisBroker
DRAMATIQ_BROKER_URL = os.getenv("REDIS_URL")
SCHEDULER_API_ENABLED = True

