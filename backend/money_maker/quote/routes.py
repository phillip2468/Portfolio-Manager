import yahooquery
from flask import Blueprint, jsonify
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP
from money_maker.models.ticker_prices import \
    ticker_price_schema as ticker_schema
from sqlalchemy import func, select, text

quote_bp = Blueprint("quote_bp", __name__, url_prefix="/quote")


@quote_bp.route("/<category>/market-change/<order>")
def market_change_by_industry(category, order):
    # TODO
    industry_sector = getattr(tP, category)
    stmt: select = select(industry_sector, func.avg(tP.market_change_percentage).label("Average"),
                          func.count(industry_sector)).where(industry_sector.is_not(None)) \
        .group_by(industry_sector).order_by(text(f""""Average" {order}"""))
    return jsonify([dict(element) for element in db.session.execute(stmt).all()])


@quote_bp.route("/<stock_symbol>")
def get_stock_info_from_database(stock_symbol):
    results = db.session.query(tP).filter(tP.symbol == stock_symbol).all()
    return ticker_schema.jsonify(results, many=True)


@quote_bp.route("/<stock_name>&period=<period>&interval=<interval>")
def get_historical_data(stock_name, period, interval):
    historical_price = yahooquery.Ticker(stock_name).history(period=period, interval=interval, adj_timezone=False)
    price_now = yahooquery.Ticker(stock_name).price[stock_name]
    this_result = {
        "priceList": [{"time": key[1], "open": value} for key, value in historical_price['open'].to_dict().items()],
        "price_now": price_now["regularMarketPrice"],
        "market_change_perc": price_now["regularMarketChangePercent"],
        "currency_symbol": price_now["currencySymbol"],
    }
    return jsonify(this_result)
