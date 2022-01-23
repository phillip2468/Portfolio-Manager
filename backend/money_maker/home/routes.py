from typing import Any

import flask
import yahooquery.ticker
from flask import Blueprint
from flask import jsonify
from money_maker.extensions import cache, db
from money_maker.helpers import market_index_ticker, object_as_dict
from money_maker.models.ticker_prices import TickerPrice as tP
from sqlalchemy import bindparam, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import ColumnElement
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
    result = [object_as_dict(element) for element in db.session.query(tP).all()]
    return jsonify(result)


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


@home_bp.route("/actively-traded")
def most_actively_traded_stocks():
    result = db.session.query(tP.symbol, ((tP.market_volume * tP.market_current_price) / tP.market_cap).label("volume"),
                              tP.market_change_percentage, tP.market_change_percentage, tP.market_current_price,
                              tP.stock_name) \
        .filter(tP.market_current_price.is_not(None)).filter(tP.market_volume.is_not(None)) \
        .filter(tP.market_current_price.is_not(None)). \
        filter(tP.market_cap.is_not(None), tP.market_cap > 10000000).filter(tP.market_change_percentage > 0) \
        .order_by(desc("volume")).limit(5).all()
    return jsonify([dict(element) for element in result])
