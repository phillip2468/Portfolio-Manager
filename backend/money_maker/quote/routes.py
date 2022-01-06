from flask import Blueprint, jsonify
from money_maker.extensions import db
from money_maker.helpers import object_as_dict
from money_maker.models.ticker_prices import TickerPrice
from sqlalchemy import func, select, text

quote_bp = Blueprint('quote_bp', __name__)


@quote_bp.route("/quote/<ticker>")
def ticker_information(ticker):
    stmt: select = select(TickerPrice).filter(TickerPrice.symbol == ticker)
    return jsonify([object_as_dict(element) for element in db.session.execute(stmt).one()])


@quote_bp.route("/quote/<category>/market-change/<order>")
def market_change_by_industry(category, order):
    industry_sector = getattr(TickerPrice, category)
    stmt: select = select(industry_sector, func.avg(TickerPrice.market_change_percentage).label("Average"),
                          func.count(industry_sector)).where(industry_sector.is_not(None)) \
        .group_by(industry_sector).order_by(text(f""""Average" {order}"""))
    return jsonify([dict(element) for element in db.session.execute(stmt).all()])
