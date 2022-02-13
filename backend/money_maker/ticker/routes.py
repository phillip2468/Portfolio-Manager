"""
This route should be thought as getting a collection of details from MANY stocks
"""
import csv

import flask
import requests
from flask import Blueprint, jsonify
from money_maker.extensions import cache, db
from money_maker.models.ticker_prices import TickerPrice as tP
from money_maker.models.ticker_prices import ticker_price_schema
from pytickersymbols import PyTickerSymbols
from sqlalchemy import func, text

ticker_bp = Blueprint("ticker_bp", __name__, url_prefix="/ticker")


@ticker_bp.route("/all", methods=["GET"])
@cache.cached(timeout=15 * 60)
def get_all_tickers() -> flask.Response:
    """
    Retrieves all tickers from the database with the relevant columns from the
    database. Note that this function is cached for 15 minutes to speed up
    the response time.
    :return: A list of dictionaries
    :rtype: flask.Response
    """
    result = db.session.query(tP).all()
    return ticker_price_schema.jsonify(result, many=True)


@ticker_bp.route("/market-change/<attribute>/<order>", methods=["GET"])
def market_change_by_attribute(attribute: str, order: str) -> flask.Response:
    """
    Given a speicific field from the TickerPrice database object, find the average
    perfomance of that specific field. Note that the attribute from TickerPrice should be
    reasonable as strange results may occur with certain fields. Refer to models/ticker_prices
    for a list of all avaliable attributes to name.
    For example a sample query could be "/market-change/sector/ASC" which would find the
    average performance for all stocks grouped by sector.
    Note that the "order" keyword should either be ASC or DESC.

    :param attribute: A field corresponding to the TickerPrice attributes.
    :type attribute: str
    :param order: ASC or DESC
    :type order: str
    :return: A list of json dictionaries.
    :rtype: flask.Response
    """
    ticker_price_field = getattr(tP, attribute)
    results = db.session.query(ticker_price_field, func.avg(tP.market_change_percentage).label("Average"),
                               func.count(ticker_price_field)).filter(ticker_price_field.isnot(None)) \
        .group_by(ticker_price_field).order_by(text(f""""Average" {order.upper()}""")).all()
    return jsonify([dict(_) for _ in results])


@ticker_bp.route("/refresh-asx-symbols", methods=["GET"])
def refresh_au_symbols() -> flask.Response:
    """
    Retrieves a list of AU stocks and inserts them into the database. Note that this function will remove
    old data associated with the stocks.
    :return: flask.Response
    """
    db.session.query(tP).filter(tP.symbol.contains(".AX")).delete(synchronize_session="fetch")

    url = 'https://asx.api.markitdigital.com/asx-research/1.0/companies/directory/file?access_token=83ff96335c2d45a094df02a206a39ff4 '

    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode("utf-8")

        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        my_list = list(cr)
        asx_tickers = ticker_price_schema.load([{"symbol": e[0] + ".AX"} for e in my_list[1:]], many=True, partial=True)
        db.session.add_all(asx_tickers)

    db.session.commit()
    result = db.session.query(tP).filter(tP.symbol.contains(".AX")).all()

    return ticker_price_schema.jsonify(result, many=True)


@ticker_bp.route("/refresh-us-symbols", methods=["GET"])
def get_american_yh_stocks():
    """
    Retrieves a list of non - AU stocks and inserts them into the database. Note that this function will remove
    old data associated with the stocks.
    :return: flask.Response
    """
    stock_data = PyTickerSymbols()

    sp500_yahoo = stock_data.get_sp_500_nyc_yahoo_tickers()
    nasdaq_yahoo = stock_data.get_nasdaq_100_nyc_yahoo_tickers()
    dow_jones = stock_data.get_dow_jones_nyc_yahoo_tickers()

    db.session.query(tP).filter(~tP.symbol.contains(".AX")).delete(synchronize_session="fetch")

    result = sp500_yahoo + nasdaq_yahoo + dow_jones
    us_tickers = ticker_price_schema.load([{"symbol": element} for element in (set(result))], many=True, partial=True)
    db.session.add_all(us_tickers)
    db.session.commit()

    result = db.session.query(tP).filter(~tP.symbol.contains(".AX")).all()
    return ticker_price_schema.jsonify(result, many=True)

