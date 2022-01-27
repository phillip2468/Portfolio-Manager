import flask.app
from flask import Flask
from money_maker.auth.routes import auth_bp
from money_maker.extensions import cache, celery, cors, db, talisman, jwt_manager, bcrypt
from money_maker.home.routes import home_bp
from money_maker.news.routes import news_stories_bp
from money_maker.quote.routes import quote_bp
from money_maker.search.routes import search_bp
from money_maker.trending.routes import trending_bp
#from money_maker.models.user import User


def create_app(testing=False) -> Flask:
    """Application factory, used to create application
    https://stackoverflow.com/questions/33089144/flask-sqlalchemy-setup-engine-configuration
    """
    app: flask.app.Flask = Flask(__name__, static_folder='../../frontend/build', static_url_path='',
                                 template_folder="../../frontend/build")
    app.config.from_object("money_maker.config")

    configure_extensions(app)
    register_blueprints(app)
    app.debug = True

    app.app_context().push()

    if testing is True:
        app.config["TESTING"] = True
    init_celery(app)

    return app


def configure_extensions(app):
    db.init_app(app)
    cache.init_app(app)
    talisman.init_app(app)
    cors.init_app(app)
    jwt_manager.init_app(app)
    bcrypt.init_app(app)


def register_blueprints(app: flask.Flask):
    app.register_blueprint(home_bp)
    app.register_blueprint(quote_bp)
    app.register_blueprint(trending_bp)
    app.register_blueprint(news_stories_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(auth_bp)


def init_celery(app: flask.app.Flask = None):
    app = app or create_app()
    celery.conf.update(app.config.get("CELERY", {}))

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
