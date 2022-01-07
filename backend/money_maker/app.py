import flask.app

from flask import Flask
from flask_cors import CORS
from money_maker.extensions import db, migrate
from money_maker.home.routes import home_bp
from money_maker.quote.routes import quote_bp
from money_maker.trending.routes import trending_bp
from flask_melodramatiq import RabbitmqBroker
import dramatiq

broker = RabbitmqBroker()
dramatiq.set_broker(broker)


def create_app(testing=False) -> Flask:
    """Application factory, used to create application
    https://stackoverflow.com/questions/33089144/flask-sqlalchemy-setup-engine-configuration
    """
    app: flask.app.Flask = Flask(__name__, static_folder='../../frontend/build', static_url_path='')
    app.config.from_object("money_maker.config")
    app.config["TESTING"] = True
    app.config["ENV"] = "development"

    configure_extensions(app)
    register_blueprints(app)
    app.debug = True

    app.app_context().push()

    CORS(app)
    if testing is True:
        app.config["TESTING"] = True

    return app


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app: flask.Flask):
    app.register_blueprint(home_bp)
    app.register_blueprint(quote_bp)
    app.register_blueprint(trending_bp)
