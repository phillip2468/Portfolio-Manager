from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

ENV = "TESTING"
SECRET_KEY = "for_testing_purposes_only"
SQLALCHEMY_DATABASE_URI = "sqlite://"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PRESERVE_CONTEXT_ON_EXCEPTION = False
DEBUG = True
TESTING = True

JWT_COOKIE_SECURE = True
JWT_TOKEN_LOCATION = ["cookies"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN-REFRESH"

# Note that in production these values would be true
JWT_COOKIE_CSRF_PROTECT = False
JWT_CSRF_IN_COOKIES = False

CELERY = {
    "broker_url": "memory://",
    "result_backend": 'rpc',
    "result_serializer": 'json'
}
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES = True
