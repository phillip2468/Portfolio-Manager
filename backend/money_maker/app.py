from flask import Flask
from flask_cors import CORS

from extensions import celery


def create_app(testing=False) -> Flask:
    """Application factory, used to create application"""
    app = Flask(__name__, static_folder='../../frontend/build', static_url_path='')
    from money_maker.home.routes import home_bp

    app.register_blueprint(home_bp)
    CORS(app)
    if testing is True:
        app.config["TESTING"] = True

    init_celery(app)
    return app


def init_celery(app=None):
    app = app or create_app()
    celery.conf.update(app.config.get("CELERY", {}))
    celery.conf.broker_url = 'redis://redistogo:e787816e73475a0d975f8c34e30a9b8a@herring.redistogo.com:9072/'
    celery.conf.result_backend = 'redis://redistogo:e787816e73475a0d975f8c34e30a9b8a@herring.redistogo.com:9072/'

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app conte1xt1"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
