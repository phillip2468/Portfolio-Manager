import flask
import yahooquery.ticker
from flask import Blueprint, current_app as app, jsonify
from requests import Response
from sqlalchemy import inspect, select, bindparam

from money_maker.extensions import db
from money_maker.helpers import sync_request
from yahooquery import Ticker

from sqlalchemy.dialects.postgresql import insert
from money_maker.models.ticker_prices import TickerPrice

from money_maker.tasks.task import add_together

home_bp = Blueprint('home_bp', __name__)


def market_index_ticker() -> Response:
    """
    Gets the code, status and title of all ASX listed stocks.
    All results are held in a list of dictionaries.
    code, status, title
    :return: List of dictionaries
    :rtype: list[dict[str, str, str]]
    """
    url: str = 'https://www.marketindex.com.au/api/v1/companies'
    return sync_request(url)


@home_bp.route('/retrieve-asx-tickers')
def asx_tickers() -> flask.Response:
    """
    Inserts asx tickers in the database.
    Returns a list of all tickers.
    """

    insert_dictionary = {
        'market_state': bindparam('status'),
        'symbol': bindparam('code') + ".AX",
        'stock_name': bindparam('title')
    }

    stmt = insert(TickerPrice).values(insert_dictionary).on_conflict_do_update(
        index_elements=['symbol'],
        set_=insert_dictionary
    )

    db.session.execute(stmt, market_index_ticker())
    db.session.commit()
    result = [object_as_dict(element) for element in (db.session.query(TickerPrice).all())]

    return jsonify(result)


@home_bp.route("/all-asx-prices")
def get_all_asx_prices() -> flask.Response:
    # https://stackoverflow.com/questions/56726689/sqlalchemy-insert-executemany-func
    # https://newbedev.com/sqlalchemy-performing-a-bulk-upsert-if-exists-update-else-insert-in-postgresql

    stmt = select(TickerPrice.symbol)
    list_symbols: list[str] = [element[0] for element in db.session.execute(stmt)]

    yh_market_information: yahooquery.Ticker.__dict__ = \
        Ticker(list_symbols, formatted=False, asynchronous=True, max_workers=100, progress=True,
               country='australia', validate=True)

    market_information = {
        'currency': default_bindparam('currency'),
        'exchange': default_bindparam('exchange'),
        'stock_name': default_bindparam('longName'),
        'market_cap': default_bindparam('marketCap'),
        'quote_type': default_bindparam('quoteType'),
        'market_change': default_bindparam('regularMarketChange'),
        'market_change_percentage': default_bindparam('regularMarketChangePercent'),
        'market_high': default_bindparam('regularMarketDayHigh'),
        'market_low': default_bindparam('regularMarketDayLow'),
        'market_open': default_bindparam('regularMarketOpen'),
        'market_previous_close': default_bindparam('regularMarketPreviousClose'),
        'market_current_price': default_bindparam('regularMarketPrice'),
        'market_volume': bindparam('regularMarketVolume', value=0),
        'symbol': bindparam('symbol')
    }
    statement = insert(TickerPrice).values(market_information)

    upsert_statement = statement.on_conflict_do_update(
        index_elements=['symbol'],
        set_=market_information
    )

    db.session.execute(upsert_statement, [element for element in yh_market_information.price.values()])
    db.session.commit()

    return jsonify(yh_market_information)


def default_bindparam(input_key: str):
    return bindparam(key=input_key, value=None)


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


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
