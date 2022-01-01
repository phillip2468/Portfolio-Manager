import datetime

import flask
import sqlalchemy.orm.scoping
import yahooquery.ticker
from flask import Blueprint, current_app as app, jsonify
from requests import Response
from sqlalchemy import inspect

from money_maker.extensions import db, base
from money_maker.helpers import sync_request
from yahooquery import Ticker

from sqlalchemy.dialects.postgresql import insert

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


def asx_tickers() -> None:
    """
    Inserts all the tickers from market index ASX.
    """
    asx_ticker = base.classes.asx_ticker

    aus_tickers = market_index_ticker()

    stmt = insert(asx_ticker).values(aus_tickers)
    stmt = stmt.on_conflict_do_nothing()
    db.session.execute(stmt)
    db.session.commit()

from sqlalchemy.sql.expression import bindparam

@home_bp.route("/all-asx-prices")
def get_all_asx_prices() -> flask.Response:
    #https://stackoverflow.com/questions/56726689/sqlalchemy-insert-executemany-func
    #https://newbedev.com/sqlalchemy-performing-a-bulk-upsert-if-exists-update-else-insert-in-postgresql
    asx_ticker = base.classes.asx_ticker

    ticker_prices = base.classes.ticker_prices

    list_of_asx_codes: list[str] = [object_as_dict(element)["code"]+".AX"
                                    for element in db.session.query(asx_ticker).all()]

    market_information_prices: yahooquery.Ticker.__dict__ = \
        Ticker(list_of_asx_codes[:2], formatted=False, asynchronous=True, max_workers=100, progress=True).price

    statement = insert(ticker_prices).values({
        'currency': bindparam('currency'),
        'exchange': bindparam('exchange'),
        'stock_name': bindparam('longName'),
        'market_cap': bindparam('marketCap'),
        'quote_type': bindparam('quoteType'),
        'market_change': bindparam('regularMarketChange'),
        'market_change_percentage': bindparam('regularMarketChangePercent'),
        'market_high': bindparam('regularMarketDayHigh'),
        'market_low': bindparam('regularMarketDayLow'),
        'market_open': bindparam('regularMarketOpen'),
        'market_previous_close': bindparam('regularMarketPreviousClose'),
        'market_current_price': bindparam('regularMarketPrice'),
        'market_volume': bindparam('regularMarketVolume'),
        'symbol': bindparam('symbol')
    })

    upsert_statement = statement.on_conflict_do_update(
        index_elements=['symbol'],
        set_={
            'currency': bindparam('currency'),
            'exchange': bindparam('exchange'),
            'stock_name': bindparam('longName'),
            'market_cap': bindparam('marketCap'),
            'quote_type': bindparam('quoteType'),
            'market_change': bindparam('regularMarketChange'),
            'market_change_percentage': bindparam('regularMarketChangePercent'),
            'market_high': bindparam('regularMarketDayHigh'),
            'market_low': bindparam('regularMarketDayLow'),
            'market_open': bindparam('regularMarketOpen'),
            'market_previous_close': bindparam('regularMarketPreviousClose'),
            'market_current_price': bindparam('regularMarketPrice'),
            'market_volume': bindparam('regularMarketVolume'),
            'market_state': bindparam('marketState')
        }
    )

    db.session.execute(upsert_statement, [element for element in market_information_prices.values()])
    db.session.commit()

    return jsonify(market_information_prices)


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
