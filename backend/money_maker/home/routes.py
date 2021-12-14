from flask import Blueprint, current_app as app

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/', methods=['GET'])
def homepage():
    return "welcome to my homepage!"
