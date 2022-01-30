"""
This route should be thought as getting a collection of details from MANY stocks
"""
import flask
from flask import Blueprint, jsonify
from money_maker.extensions import cache, db
from money_maker.models.ticker_prices import TickerPrice as tP
from money_maker.models.ticker_prices import ticker_price_schema
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
