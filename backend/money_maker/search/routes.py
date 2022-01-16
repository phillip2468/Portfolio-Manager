from flask import Blueprint, jsonify
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP

search_bp = Blueprint("search_bp", __name__, url_prefix="/search")


@search_bp.route("")
def get_all_companies():
    results = db.session.query(tP.stock_id.label("key"), tP.stock_name, tP.symbol,
                               tP.market_current_price.label("price"), tP.market_change_percentage.label("change")). \
        order_by(tP.stock_name).filter(tP.market_current_price.isnot(None)).all()
    return jsonify([dict(element) for element in results])
