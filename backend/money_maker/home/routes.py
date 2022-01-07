import datetime
from typing import Any

import flask
import pytz
import yahooquery.ticker
from flask import Blueprint
from flask import current_app as app
from flask import jsonify
from money_maker.extensions import db
from money_maker.helpers import market_index_ticker, object_as_dict
from money_maker.models.ticker_prices import TickerPrice
from money_maker.tasks.task import add_together
from sqlalchemy import asc, bindparam, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import ColumnElement
from sqlalchemy_utils import get_columns
from yahooquery import Ticker

home_bp = Blueprint('home_bp', __name__)


@home_bp.route("/retrieve-asx-tickers")
def asx_tickers() -> flask.Response:
    """
    Inserts asx tickers in the database.
    Returns a list of all tickers.
    """
    print(add_together.delay())

    insert_dictionary: dict[str, ColumnElement[Any]] = {
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

    stmt = select(func.max(TickerPrice.last_updated))
    last_updated_stock = db.session.execute(stmt).one()[0]

    # This is so the database isn't queried every time.
    if pytz.utc.localize(last_updated_stock) + datetime.timedelta(minutes=1) > datetime.datetime.now(pytz.utc):
        return jsonify([object_as_dict(element) for element in db.session.query(TickerPrice).all()])

    list_asx_symbols = select(TickerPrice.symbol).order_by(asc(TickerPrice.symbol))
    list_symbols: list[str] = [element[0] for element in db.session.execute(list_asx_symbols)]

    yh_market_information: yahooquery.Ticker.__dict__ = \
        Ticker(list_symbols, formatted=False, asynchronous=True, max_workers=min(100, len(list_symbols)),
               progress=True,
               country='australia').get_modules('price summaryProfile')

    list_of_market_info = [{**element["price"], **element["summaryProfile"]} for element in
                           yh_market_information.values() if type(element) == dict and element.keys() in "price"]
    db.session.execute(TickerPrice.__table__.insert(), list_of_market_info)
    db.session.commit()

    return jsonify(list_of_market_info)


@home_bp.route('/trending-tickers')
def trending_tickers() -> flask.Response:
    """
    Provides a dictionary set of tickers containing
    relevant data to the date. Note that this only returns
    US trending stocks.
    :return: flask.Response
    """
    trending_yh_tickers: dict = yahooquery.get_trending()

    # This gets rid of crypto related items
    trending_securities = [element["symbol"] for element in
                           trending_yh_tickers["quotes"] if "-" not in element["symbol"]]

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
