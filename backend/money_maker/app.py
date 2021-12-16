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

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
