import flask
import yahooquery.ticker
from flask import Blueprint, jsonify, make_response
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP
from sqlalchemy import desc
from yahooquery import Ticker

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/trending-tickers')
def trending_tickers() -> flask.Response:
    """
    Provides a dictionary set of tickers containing
    relevant data to the date. Note that this only returns
    US trending stocks.

    Returns:
        A response containing a dictionary of the wanted keys of the stocks.
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
def most_actively_traded_stocks() -> flask.Response:
    """
    Provides a general overview for popular stocks that are traded using a simple
    formula of volumne * current price / market cap. Only provides the first
    5 results.
    Returns:
        A response containing each stock, with their relevant details
    """
    if len(db.session.query(tP).all()) == 0:
        return make_response(jsonify({"error": "No stocks in the database!"}), 400)

    result = db.session.query(tP.symbol, ((tP.market_volume * tP.market_current_price) / tP.market_cap).label("volume"),
                              tP.market_change_percentage, tP.market_change_percentage, tP.market_current_price,
                              tP.stock_name) \
        .filter(tP.market_current_price.is_not(None)).filter(tP.market_volume.is_not(None)) \
        .filter(tP.market_current_price.is_not(None)). \
        filter(tP.market_cap.is_not(None), tP.market_cap > 10000000).filter(tP.market_change_percentage > 0) \
        .order_by(desc("volume")).limit(5).all()
    return jsonify([dict(element) for element in result])
