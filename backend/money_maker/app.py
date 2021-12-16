import flask.app

from flask import Flask
from flask_cors import CORS

from extensions import celery
from money_maker.extensions import db, celery, base


def create_app(testing=False) -> Flask:
    """Application factory, used to create application"""
    app: flask.app.Flask = Flask(__name__, static_folder='../../frontend/build', static_url_path='')
    from money_maker.home.routes import home_bp
    app.debug = True

    app.app_context().push()
    #db.init_app(app)
    #base.__prepare__(db.engine, reflect=True)

    app.register_blueprint(home_bp)
    CORS(app)
    if testing is True:
        app.config["TESTING"] = True

    init_celery(app)
    return app


def init_celery(app: flask.app.Flask = None) -> celery:
    app = app or create_app()
    celery.conf.update(app.config.get("CELERY", {}))
    celery.conf.broker_url = 'redis://:p4f59a8e2e5f342d5eba3e0f0c6d7e2248726b02b3ebf626676b67d2982281882@ec2-54-80-214-228.compute-1.amazonaws.com:8059'
    celery.conf.result_backend = 'redis://:p4f59a8e2e5f342d5eba3e0f0c6d7e2248726b02b3ebf626676b67d2982281882@ec2-54-80-214-228.compute-1.amazonaws.com:8059'

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
