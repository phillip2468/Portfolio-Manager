from flask import Flask
from flask_cors import CORS

from money_maker.home.routes import home_bp


def create_worker_app():
    app = Flask(__name__)
    CORS(app)

    return app


def create_app():
    app = Flask(__name__, static_folder='../../frontend/build', static_url_path='')
    app.register_blueprint(home_bp)
    CORS(app)

    return app
