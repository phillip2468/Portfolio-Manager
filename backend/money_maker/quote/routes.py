"""
This route should be thought as getting specific details for ONE
particular symbol
"""
import flask
import pandas as pd
import yahooquery
from flask import Blueprint, jsonify, make_response

from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP
from money_maker.models.ticker_prices import \
    ticker_price_schema as ticker_schema

quote_bp = Blueprint("quote_bp", __name__, url_prefix="/quote")

error_message = "No data found, symbol may be delisted"


@quote_bp.route("/<stock_symbol>", methods=["GET"])
def get_stock_info_from_database(stock_symbol: str) -> flask.Response:
    """
    Given a stock symbol from the url, return the matching information
    pertaining to the company from the database. Refer to TickerPrice
    for all attributes that are returned for a stock symbol.
    Args:
        stock_symbol: The stock symbol

    Returns:
        A flask response object containing a TickerPrice object and status code

    """
    stock_information = db.session.query(tP).filter(tP.symbol == stock_symbol).one_or_none()
    if stock_information is None:
        return make_response(jsonify({"error": "Invalid stock symbol"}), 400)

    return ticker_schema.jsonify(stock_information)


@quote_bp.route("/<stock_symbol>&period=<period>&interval=<interval>")
def get_historical_data(stock_symbol: str, period: str, interval: str) -> flask.Response:
    """
    Given a specific ticker, find the historical pricing of this company (uses the opening price as its data points)
    Note that due to limitations with the yahoo finance library, some combinations of periods
    and time intervals are not avaliable. \n
    Options for periods include ['1d', '5d', '7d', '60d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'] \n
    Options for interval include ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'] \n

    Args:
        stock_symbol: The ticker for the company
        period: Length of time as indicated by the options above
        interval: Time between data points as indicated by the options above

    Returns:
        A custom dictionary (refer to custom_dict) for specific key, values.
    """

    historical_price = yahooquery.Ticker(stock_symbol).history(period=period, interval=interval, adj_timezone=False)
    price_now = yahooquery.Ticker(stock_symbol).price[stock_symbol]
    if not isinstance(historical_price, pd.DataFrame):
        return make_response(jsonify({"err": error_message}), 400)
    custom_dict = {
        "priceList": [{"time": key[1], "open": value} for key, value in historical_price['open'].to_dict().items()],
        "price_now": price_now["regularMarketPrice"],
        "market_change_perc": price_now["regularMarketChangePercent"],
        "currency_symbol": price_now["currencySymbol"],
    }
    return jsonify(custom_dict)
