import datetime
import sys
from typing import Any

import flask
import pytz
import yahooquery.ticker
from flask import Blueprint
from flask import current_app as app
from flask import jsonify
from money_maker.extensions import cache, db
from money_maker.helpers import market_index_ticker, object_as_dict
from money_maker.models.ticker_prices import TickerPrice as tP
# from money_maker.tasks.task import add_together
from sqlalchemy import asc, bindparam, desc, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import ColumnCollection, ColumnElement
from sqlalchemy_utils import get_columns
from yahooquery import Ticker

home_bp = Blueprint('home_bp', __name__)


@home_bp.route("/retrieve-asx-tickers")
def asx_tickers() -> flask.Response:
    """
    Inserts asx tickers in the database.
    Returns a list of all tickers.
    """

    insert_dictionary: dict[str, ColumnElement[Any]] = {
        'market_state': bindparam('status'),
        'symbol': bindparam('code') + ".AX",
        'stock_name': bindparam('title')
    }

    stmt = insert(tP).values(insert_dictionary).on_conflict_do_update(
        index_elements=['symbol'],
        set_=insert_dictionary
    )

    db.session.execute(stmt, market_index_ticker())
    db.session.commit()
    result = [object_as_dict(element) for element in (db.session.query(tP).all())]

    return jsonify(result)


@home_bp.route("/all-asx-prices")
@cache.cached(timeout=15 * 60)
def get_all_asx_prices() -> flask.Response:
    # https://stackoverflow.com/questions/56726689/sqlalchemy-insert-executemany-func
    # https://newbedev.com/sqlalchemy-performing-a-bulk-upsert-if-exists-update-else-insert-in-postgresql
    stmt = select(func.max(tP.last_updated))
    last_updated_stock = db.session.execute(stmt).one()[0]

    # This is so the database isn't queried every time.
    if pytz.utc.localize(last_updated_stock) + datetime.timedelta(minutes=15) > datetime.datetime.now(pytz.utc):
        return jsonify([object_as_dict(element) for element in db.session.query(tP).all()])

    list_asx_symbols = select(tP.symbol).order_by(asc(tP.symbol))
    list_symbols: list[str] = [element[0] for element in db.session.execute(list_asx_symbols)]

    yh_market_information: yahooquery.Ticker.__dict__ = \
        Ticker(list_symbols, formatted=True, asynchronous=True, max_workers=min(100, len(list_symbols)),
               progress=True,
               country='australia').get_modules('price summaryProfile')

    formatted_yh_information = []
    for element in yh_market_information.values():
        if type(element) == dict and len(element.keys()) == 2:
            raw_dictionary = {**element["price"], **element["summaryProfile"]}
            formatted_yh_information.append({key: value if type(value) != dict else value["raw"] if len(value) > 0
            else None for (key, value) in raw_dictionary.items()})

    market_information = {
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

    stmt = insert(tP).values(market_information)

    on_conflict_statement = stmt.on_conflict_do_update(
        index_elements=['symbol'],
        set_=market_information
    )

    db.session.execute(on_conflict_statement, formatted_yh_information)
    db.session.commit()

    return jsonify(formatted_yh_information)


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


@home_bp.route('/past-data')
def past_data():
    tickers = Ticker('CBA.AX').history(period='7d')
    print(tickers)
    print(tickers.to_dict('list'))
    print(sys.getsizeof(tickers))
    return jsonify(tickers.to_dict('records'))


@home_bp.route("/actively-traded")
def most_actively_traded_stocks():
    result = db.session.query(tP.symbol, ((tP.market_volume * tP.market_current_price) / tP.market_cap).label("volume"),
                              tP.market_change_percentage, tP.market_change_percentage, tP.market_current_price, tP.stock_name)\
        .filter(tP.market_current_price.is_not(None)).filter(tP.market_volume.is_not(None))\
        .filter(tP.market_current_price.is_not(None)).\
        filter(tP.market_cap.is_not(None), tP.market_cap > 10000000).filter(tP.market_change_percentage > 0)\
        .order_by(desc("volume")).limit(5).all()
    return jsonify([dict(element) for element in result])



@home_bp.route('/')
def serve():
    return app.send_static_file('index.html')
