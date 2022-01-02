import flask_sqlalchemy
import sqlalchemy
from celery import Celery
from flask_migrate import Migrate
from sqlalchemy.ext.automap import automap_base

celery = Celery()
db: flask_sqlalchemy.SQLAlchemy = flask_sqlalchemy.SQLAlchemy(engine_options={
    "executemany_mode": 'values',
    "executemany_values_page_size": 10000,
    "executemany_batch_page_size": 500
})
migrate = Migrate()
base: sqlalchemy.ext.automap = automap_base()

