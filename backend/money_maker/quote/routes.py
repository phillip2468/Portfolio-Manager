from flask import Blueprint, jsonify
from money_maker.extensions import cache, db
from money_maker.models.ticker_prices import TickerPrice as tP
from sqlalchemy import func, select, text

quote_bp = Blueprint("quote_bp", __name__, url_prefix="/quote")


@quote_bp.route("/<ticker>")
def ticker_information(ticker):
    return jsonify([dict(element) for element in db.session.query(tP.symbol).filter(tP.symbol == ticker).all()])


@quote_bp.route("/<category>/market-change/<order>")
def market_change_by_industry(category, order):
    industry_sector = getattr(tP, category)
    stmt: select = select(industry_sector, func.avg(tP.market_change_percentage).label("Average"),
                          func.count(industry_sector)).where(industry_sector.is_not(None)) \
        .group_by(industry_sector).order_by(text(f""""Average" {order}"""))
    return jsonify([dict(element) for element in db.session.execute(stmt).all()])


@quote_bp.route("/search")
@cache.cached(timeout=600)
def get_all_companies():
    results = db.session.query(tP.stock_id.label("key"), tP.stock_name.label("value"), tP.symbol,
                               tP.market_current_price.label("price"), tP.market_change_percentage.label("change")).\
        order_by(tP.stock_name).filter(tP.market_current_price.isnot(None)).all()
    return jsonify([dict(element) for element in results])
