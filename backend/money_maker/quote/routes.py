from flask import Blueprint, jsonify
from money_maker.extensions import db
from money_maker.helpers import object_as_dict
from money_maker.models.ticker_prices import TickerPrice
from sqlalchemy import select, func, alias, text

quote_bp = Blueprint('quote_bp', __name__)


@quote_bp.route("/quote/<ticker>")
def ticker_information(ticker):
    stmt: select = select(TickerPrice).filter(TickerPrice.symbol == ticker)
    return jsonify([object_as_dict(element) for element in db.session.execute(stmt).one()])


@quote_bp.route("/quote/industry/market-change/<order>")
def market_change_by_industry(order):
    stmt: select = select(TickerPrice.industry, func.avg(TickerPrice.market_change_percentage).label("Average"),
                          func.count(TickerPrice.industry)).where(TickerPrice.industry.is_not(None))\
                        .group_by(TickerPrice.industry).order_by(text(f""""Average" {order}"""))
    return jsonify([element._asdict() for element in db.session.execute(stmt).all()])
