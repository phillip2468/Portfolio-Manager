from flask import Blueprint, jsonify
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP
from sqlalchemy import desc

search_bp = Blueprint("search_bp", __name__, url_prefix="/search")


@search_bp.route("")
def get_all_companies():
    results = db.session.query(tP.stock_id.label("key"), tP.stock_name, tP.symbol,
                               tP.market_current_price.label("price"), tP.market_change_percentage.label("change")). \
        order_by(tP.stock_name).filter(tP.market_current_price.isnot(None)).all()
    return jsonify([dict(element) for element in results])


@search_bp.route("/<keyword>")
def search_for_companies(keyword):
    keyword = "%{}%".format(keyword).upper()
    results = db.session.query(tP.stock_id.label("key"), tP.stock_name, tP.symbol,
                               tP.market_current_price.label("price"), tP.market_change_percentage.label("change"))\
        .filter((tP.stock_name.ilike(keyword)) | (tP.symbol.ilike(keyword))).order_by(desc(tP.market_cap)).limit(5).all()
    return jsonify([dict(e) for e in results])
