from celery import Celery
from flask import Flask
from flask_cors import CORS

from backend.extensions import register_extensions
from .home.routes import home_bp
from os import environ


def create_app():
    app = Flask(__name__, static_folder='../../frontend/build', static_url_path='')
    app.register_blueprint(home_bp)
    CORS(app)

    return app


def create_worker_app():
    app = Flask(__name__)
    CORS(app)

    register_extensions(app, worker=True)
    return app
