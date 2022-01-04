import datetime
from typing import Any

import flask
import yahooquery.ticker
import pytz

from flask import Blueprint, current_app as app, jsonify
from requests import Response
from sqlalchemy import inspect, select, bindparam, asc, func
from sqlalchemy.sql.elements import BindParameter
from sqlalchemy.sql.type_api import TypeEngine

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

    stmt: select = select(func.max(TickerPrice.last_updated))
    last_updated_stock = db.session.execute(stmt).one()[0]

    # This is so the database isn't queried every time.
    if datetime.datetime.now(pytz.UTC) - last_updated_stock < datetime.timedelta(minutes=15):
        return jsonify([object_as_dict(element) for element in db.session.query(TickerPrice).all()])

    list_asx_symbols = select(TickerPrice.symbol).order_by(asc(TickerPrice.symbol))
    list_symbols: list[str] = [element[0] for element in db.session.execute(list_asx_symbols)]

    yh_market_information: yahooquery.Ticker.__dict__ = \
        Ticker(list_symbols, formatted=True, asynchronous=True, max_workers=min(100, len(list_symbols)),
               progress=True,
               country='australia').get_modules('price summaryProfile')

    market_information: dict[str | Any, BindParameter[TypeEngine[Any] | Any] | Any] = {
        'currency': bindparam('currency', value=None),
        'city': bindparam('city', value=None),
        'industry': bindparam('industry', value=None),
        'zip_code': bindparam('zip', value=None),
        'sector': bindparam('sector', value=None),
        'country': bindparam('country', value=None),
        'exchange': bindparam('exchange', value=None),
        'stock_name': bindparam('longName', value=None),
        'market_cap': bindparam('marketCap', value=None),
        'quote_type': bindparam('quoteType', value=None),
        'market_change': bindparam('regularMarketChange', value=None),
        'market_change_percentage': bindparam('regularMarketChangePercent', value=None),
        'market_high': bindparam('regularMarketDayHigh', value=None),
        'market_low': bindparam('regularMarketDayLow', value=None),
        'market_open': bindparam('regularMarketOpen', value=None),
        'market_previous_close': bindparam('regularMarketPreviousClose', value=None),
        'market_current_price': bindparam('regularMarketPrice', value=None),
        'market_volume': bindparam('regularMarketVolume', value=None),
        'symbol': bindparam('symbol')
    }
    statement = insert(TickerPrice).values(market_information)

    upsert_statement = statement.on_conflict_do_update(
        index_elements=['symbol'],
        set_=market_information
    )

    formatted_yh_information = []
    for stock_ticker in yh_market_information.values():
        if type(stock_ticker) == dict:
            new_dictionary = {}
            for module in stock_ticker.values():
                for value in module.items():
                    if type(value[1]) != dict:
                        new_dictionary[value[0]] = value[1]
                    elif len(module[value[0]]) > 0:
                        new_dictionary[value[0]] = value[1]["raw"]
                    else:
                        new_dictionary[value[0]] = None
            formatted_yh_information.append(new_dictionary)

    db.session.execute(upsert_statement, formatted_yh_information)
    db.session.commit()

    return jsonify(formatted_yh_information)


@home_bp.route('/quote/<ticker>')
def ticker_information(ticker):
    stmt: select = select(TickerPrice).filter(TickerPrice.symbol == ticker)
    return jsonify([object_as_dict(element) for element in db.session.execute(stmt).one()])


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
