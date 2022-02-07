import flask.app
from flask import Flask

from money_maker.auth.routes import auth_bp
from money_maker.extensions import (bcrypt, cache, celery, cors, db,
                                    jwt_manager, marshmallow)
from money_maker.home.routes import home_bp
from money_maker.news.routes import news_stories_bp
from money_maker.portfolio.routes import portfolio_bp
from money_maker.quote.routes import quote_bp
from money_maker.search.routes import search_bp
from money_maker.ticker.routes import ticker_bp
from money_maker.trending.routes import trending_bp
from money_maker.watchlist.routes import watchlist_bp


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
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    if testing is True:
        app.config["TESTING"] = True
    init_celery(app)

    return app


def configure_extensions(app):
    db.init_app(app)
    cache.init_app(app)
    cors.init_app(app)
    jwt_manager.init_app(app)
    bcrypt.init_app(app)
    marshmallow.init_app(app)


def register_blueprints(app: flask.Flask):
    app.register_blueprint(home_bp)
    app.register_blueprint(quote_bp)
    app.register_blueprint(trending_bp)
    app.register_blueprint(news_stories_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ticker_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(watchlist_bp)


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


class HTTPMethodOverrideMiddleware(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
        if method in self.allowed_methods:
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)
