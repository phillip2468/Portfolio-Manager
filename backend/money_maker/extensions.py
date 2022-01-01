import flask_sqlalchemy
import sqlalchemy
from celery import Celery
from sqlalchemy.ext.automap import automap_base

celery = Celery()
db: flask_sqlalchemy.SQLAlchemy = flask_sqlalchemy.SQLAlchemy()
base: sqlalchemy.ext.automap = automap_base()

