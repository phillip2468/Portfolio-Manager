import yahooquery
from flask import Blueprint, jsonify
from money_maker.extensions import cache, db
from money_maker.models.ticker_prices import TickerPrice as tP
from sqlalchemy import func, select, text

quote_bp = Blueprint("quote_bp", __name__, url_prefix="/quote")


@quote_bp.route("/<category>/market-change/<order>")
def market_change_by_industry(category, order):
    industry_sector = getattr(tP, category)
    stmt: select = select(industry_sector, func.avg(tP.market_change_percentage).label("Average"),
                          func.count(industry_sector)).where(industry_sector.is_not(None)) \
        .group_by(industry_sector).order_by(text(f""""Average" {order}"""))
    return jsonify([dict(element) for element in db.session.execute(stmt).all()])


@quote_bp.route("/<stock_name>")
def get_stock_info(stock_name):
    stmt = select(tP.__table__.columns).where(tP.symbol == stock_name)
    return jsonify([dict(element) for element in db.session.execute(stmt).all()])


@quote_bp.route("/?<stock_name>&period=<period>&interval=<interval>")
def get_historical_data(stock_name, period, interval):
    result = yahooquery.Ticker(stock_name).history(period=period, interval=interval)
    print(result)
