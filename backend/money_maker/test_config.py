from dotenv import load_dotenv

load_dotenv()

ENV = "TESTING"
SECRET_KEY = "for_testing_purposes_only"
SQLALCHEMY_DATABASE_URI = "sqlite://"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PRESERVE_CONTEXT_ON_EXCEPTION = False
DEBUG = True
TESTING = True
