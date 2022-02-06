"""
Provides a simple way for users to search stocks in the database.
Customise the options in the route to reflect this.
"""
import flask
from flask import Blueprint
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP
from money_maker.models.ticker_prices import ticker_price_schema

search_bp = Blueprint("search_bp", __name__, url_prefix="/search")


@search_bp.route("/<keyword>", methods=['GET'])
def search_company(keyword: str) -> flask.Response:
    """
    A function which takes in a keyword from the url and
    searches the database. Makes use of the "ilkie" function
    in sqlalchemy to match items. Only returns the first 4
    results.

    :param keyword: The search term query
    :type keyword: String
    :return: The result as a list of dictionaries.
    :rtype: flask.Response
    """
    keyword = "%{}%".format(keyword).upper()
    results = db.session.query(tP.stock_id, tP.stock_name, tP.symbol, tP.market_current_price,
                               tP.market_change_percentage) \
        .filter((tP.stock_name.ilike(keyword)) | (tP.symbol.ilike(keyword))) \
        .order_by(tP.market_volume.desc().nullslast()).limit(4).all()
    return ticker_price_schema.jsonify(results, many=True)
