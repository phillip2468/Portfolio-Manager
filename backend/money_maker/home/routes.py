import datetime
import time

import flask
import yahooquery.ticker
from flask import Blueprint, current_app as app, jsonify
from requests import Response

from money_maker.extensions import db
from money_maker.helpers import sync_request
from yahooquery import Ticker

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
    time1 = datetime.datetime.now()
    these_tickers = [element['code'] + '.AX' for element in get_aus_tickers()[:100]]
    data: yahooquery.ticker.Ticker.__dict__ = Ticker(these_tickers, formatted=False, asynchronous=True).price
    wanted_keys = ['symbol', 'regularMarketPrice', 'regularMarketChange', 'currencySymbol', 'marketCap']
    #data_as_list = [element for element in data]
    for key, value in data.items():
        new_dict = {k: value[k] for k in set(wanted_keys) & set(value.keys())}
        data[key] = new_dict

    print(datetime.datetime.now() - time1)
    print(len(data))
    return jsonify(get_aus_tickers())


@home_bp.route('/')
def serve():
    return app.send_static_file('index.html')

