from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_folder='../../frontend/build', static_url_path='')
    from money_maker.home.routes import home_bp
    app.register_blueprint(home_bp)
    CORS(app)

    return app
