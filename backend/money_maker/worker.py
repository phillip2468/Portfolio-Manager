from __future__ import absolute_import

from flask import Flask
from flask_cors import CORS


def create_worker_app():
    app = Flask(__name__)
    CORS(app)

    return app
