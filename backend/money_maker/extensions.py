import flask_sqlalchemy
from celery import Celery
from sqlalchemy.ext.automap import automap_base
import sqlalchemy.orm.decl_api

celery = Celery()
db: flask_sqlalchemy.SQLAlchemy = flask_sqlalchemy.SQLAlchemy()
base: sqlalchemy.orm.decl_api.DeclarativeMeta = automap_base()

