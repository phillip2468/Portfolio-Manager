import datetime
import functools
import time

import flask
import yahooquery.ticker
from flask import Blueprint, current_app as app, jsonify
from requests import Response

from money_maker.extensions import db, base
from money_maker.helpers import sync_request
from yahooquery import Ticker

from sqlalchemy.dialects.postgresql import insert

from money_maker.tasks.task import add_together

home_bp = Blueprint('home_bp', __name__)


def get_aus_tickers() -> Response:
    """
    Gets the code, status and title of all ASX listed stocks.
    All results are held in a list of dictionaries.
    code, status, title
    :return: List of dictionaries
    :rtype: list[dict[str, str, str]]
    """
    url: str = 'https://www.marketindex.com.au/api/v1/companies'
    return sync_request(url)


@home_bp.route('/aus-tickers', methods=['GET'])
def asx_tickers() -> flask.Response:
    """
    Packages the response to a json format.
    :return: The list of dictionaries containing the tickers.
    :rtype: flask.Response
    """
    asx_ticker = base.classes.asx_ticker

    aus_tickers = get_aus_tickers()
    all_asx_tickers: list[str] = [element['code'] + '.AX' for element in aus_tickers]
    stmt = insert(asx_ticker).values(aus_tickers)
    stmt = stmt.on_conflict_do_nothing()
    print(aus_tickers[0])
    db.session.execute(stmt)
    db.session.commit()

    
    # data: yahooquery.ticker.Ticker.__dict__ = Ticker(all_asx_tickers, formatted=False, asynchronous=True).price
    # wanted_keys: list[str] = ['symbol', 'regularMarketPrice', 'regularMarketChange', 'currencySymbol', 'marketCap']
    #
    # # This gets all the keys necessary
    # for key, value in data.items():
    #     new_dict = {k: value[k] for k in set(wanted_keys) & set(value.keys())}
    #     data[key] = new_dict
    #
    # for key, value in data.items():
    #     print(value)

    return jsonify(all_asx_tickers)


def get_all_asx_prices() -> flask.Response:
    pass


@home_bp.route('/trending-tickers')
def trending_tickers() -> flask.Response:
    """
    Provides a dictionary set of tickers containing
    relevant data to the date. Note that this only returns
    US trending stocks.
    :return: flask.Response
    """
    data: dict = yahooquery.get_trending()

    # This gets rid of crypto related items
    trending_securities = [element["symbol"] for element in data["quotes"] if "-" not in element["symbol"]]
    data: yahooquery.ticker.Ticker.__dict__ = Ticker(trending_securities).price
    wanted_keys = ['symbol', 'regularMarketPrice', 'regularMarketChange',
                   'regularMarketDayHigh', 'regularMarketDayLow', 'marketCap', 'shortName']

    for key, value in data.items():
        new_dict = {k: value[k] for k in set(wanted_keys) & set(value.keys())}
        data[key] = new_dict

    return jsonify(data)


@home_bp.route('/')
def serve():
    return app.send_static_file('index.html')
