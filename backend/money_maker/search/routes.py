from flask import Blueprint, jsonify
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP

search_bp = Blueprint("search_bp", __name__, url_prefix="/search")


@search_bp.route("/<keyword>")
def search_for_companies(keyword):
    keyword = "%{}%".format(keyword).upper()
    results = db.session.query(tP.stock_id.label("key"), tP.stock_name, tP.symbol,
                               tP.market_current_price.label("price"), tP.market_change_percentage.label("change"))\
        .filter((tP.stock_name.ilike(keyword)) | (tP.symbol.ilike(keyword)))\
        .order_by(tP.market_volume.desc().nullslast()).limit(4).all()
    return jsonify([dict(e) for e in results])
