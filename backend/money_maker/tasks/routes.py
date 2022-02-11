from flask import Blueprint, jsonify
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP
from money_maker.models.ticker_prices import ticker_price_schema
from sqlalchemy import asc, bindparam, insert, select
from yahooquery import Ticker

task_bp = Blueprint("task_bp", __name__, url_prefix="/task")


# noinspection DuplicatedCode
@task_bp.route("", methods=["GET"])
def update_stocks():
    """
    Note that this function will only update the first 100 stocks.
    :return:
    """
    list_all_symbols = select(tP.symbol).order_by(asc(tP.symbol))
    list_symbols = [element[0] for element in db.session.execute(list_all_symbols)]

    if len(list_symbols) == 0:
        return jsonify({"error": "no stocks found"}), 400

    yh_market_information = Ticker(list_symbols[:100],
                                   formatted=False, asynchronous=True)\
        .get_modules('price summaryProfile')

    formatted_yh_information = []
    for element in yh_market_information.values():
        if type(element) == dict and len(element.keys()) == 2:
            raw_dictionary = {**element["price"], **element["summaryProfile"]}
            formatted_yh_information.append({key: value if type(value) != dict else value["raw"] if len(value) > 0
            else None for (key, value) in raw_dictionary.items()})

    market_information = {
        'currency': bindparam('currency', value=None),
        'city': bindparam('city', value=None),
        'industry': bindparam('industry', value=None),
        'zip_code': bindparam('zip', value=None),
        'sector': bindparam('sector', value=None),
        'country': bindparam('country', value=None),
        'exchange': bindparam('exchange', value=None),
        'stock_name': bindparam('longName', value=None),
        'market_cap': bindparam('marketCap', value=None),
        'quote_type': bindparam('quoteType', value=None),
        'market_change': bindparam('regularMarketChange', value=None),
        'market_change_percentage': bindparam('regularMarketChangePercent', value=None),
        'market_high': bindparam('regularMarketDayHigh', value=None),
        'market_low': bindparam('regularMarketDayLow', value=None),
        'market_open': bindparam('regularMarketOpen', value=None),
        'market_previous_close': bindparam('regularMarketPreviousClose', value=None),
        'market_current_price': bindparam('regularMarketPrice', value=None),
        'market_volume': bindparam('regularMarketVolume', value=None),
        'symbol': bindparam('symbol')
    }

    db.session.query(tP).delete(synchronize_session="fetch")

    # noinspection PyTypeChecker
    stmt = insert(tP).values(market_information)
    db.session.execute(stmt, formatted_yh_information)

    db.session.commit()
    results = db.session.query(tP).all()

    return ticker_price_schema.jsonify(results, many=True)
