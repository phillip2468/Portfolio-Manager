import flask
from flask import Blueprint, current_app as app, jsonify
from requests import Response

from money_maker.helpers import sync_request

from money_maker.tasks.task import add_together

home_bp = Blueprint('home_bp', __name__)


def get_aus_tickers() -> Response:
    """
    Gets the code, status and title of all ASX listed stocks.
    All results are held in a list of dictionaries.
    :return: List of dictionaries
    :rtype: list[dict[str, str, str]]
    """
    url: str = 'https://www.marketindex.com.au/api/v1/companies'
    return sync_request(url)


@home_bp.route('/aus_tickers', methods=['GET'])
def asx_tickers() -> flask.Response:
    """
    Packages the response to a json format.
    :return: The list of dictionaries containing the tickers.
    :rtype: flask.Response
    """
    res = add_together.delay()
    print(res)
    print('Hash key is above!')
    return jsonify(get_aus_tickers())


@home_bp.route('/')
def serve():
    res = add_together.delay()
    print(res)
    return app.send_static_file('index.html')

