import flask
import yahooquery
from flask import Blueprint, jsonify
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP
from money_maker.models.ticker_prices import \
    ticker_price_schema as ticker_schema
from sqlalchemy import func, text

quote_bp = Blueprint("quote_bp", __name__, url_prefix="/quote")


@quote_bp.route("/market-change/industry/<order>", methods=["GET"])
def market_change_by_industry(order: str) -> flask.Response:
    """
    Provides the average performance for tickers within a specific industry,
    given the order. Note that the order keyword should either be
    ASC or DESC.


    :param order: ASC or DESC
    :type order: str
    :return: A list of dictionaries.
    :rtype: flask.Response
    """
    results = db.session.query(tP.industry, func.avg(tP.market_change_percentage).label("Average"),
                               func.count(tP.industry)).filter(tP.industry.isnot(None))\
        .group_by(tP.industry).order_by(text(f""""Average" {order.upper()}""")).all()
    return jsonify([dict(e) for e in results])


@quote_bp.route("/market-change/sector/<order>", methods=["GET"])
def market_change_by_industry(order: str) -> flask.Response:
    """
    Provides the average performance for tickers within a specific sector,
    given the order. Note that the order keyword should either be
    ASC or DESC.


    :param order: ASC or DESC
    :type order: str
    :return: A list of dictionaries.
    :rtype: flask.Response
    """
    results = db.session.query(tP.sector, func.avg(tP.market_change_percentage).label("Average"),
                               func.count(tP.sector)).filter(tP.sector.isnot(None)) \
        .group_by(tP.sector).order_by(text(f""""Average" {order.upper()}""")).all()
    return jsonify([dict(e) for e in results])


@quote_bp.route("/<stock_symbol>", methods=["GET"])
def get_stock_info_from_database(stock_symbol: str) -> flask.Response:
    """
    Using the keyword from the url, return the matching information
    about a certain company from the database. Refer to the TickerPrice
    model to see which attributes are returned.


    :param stock_symbol: The ticker for the company
    :type stock_symbol: str
    :return: A flask response object (list of dictionaries)
    :rtype: flask.Response
    """
    results: list[tP] = db.session.query(tP).filter(tP.symbol == stock_symbol).all()
    return ticker_schema.jsonify(results, many=True)


@quote_bp.route("/<stock_name>&period=<period>&interval=<interval>")
def get_historical_data(stock_name, period, interval):
    historical_price = yahooquery.Ticker(stock_name).history(period=period, interval=interval, adj_timezone=False)
    price_now = yahooquery.Ticker(stock_name).price[stock_name]
    this_result = {
        "priceList": [{"time": key[1], "open": value} for key, value in historical_price['open'].to_dict().items()],
        "price_now": price_now["regularMarketPrice"],
        "market_change_perc": price_now["regularMarketChangePercent"],
        "currency_symbol": price_now["currencySymbol"],
    }
    return jsonify(this_result)
