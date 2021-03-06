from __future__ import absolute_import, unicode_literals

import yahooquery
from celery import shared_task
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP
from sqlalchemy import asc, bindparam, insert, select
from sqlalchemy.dialects.postgresql import insert
from yahooquery import Ticker

from money_maker.ticker.routes import get_american_yh_stocks, refresh_au_symbols


@shared_task()
def update_yh_stocks():
    get_american_yh_stocks()
    refresh_au_symbols()
    list_symbols = select(tP.symbol).order_by(asc(tP.symbol))
    list_symbols: list[str] = [element[0] for element in db.session.execute(list_symbols)]

    yh_market_information: yahooquery.Ticker.__dict__ = \
        Ticker(list_symbols, formatted=True, asynchronous=True, max_workers=min(100, len(list_symbols)),
               progress=True).get_modules('price summaryProfile')

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


def non_celery_update_yh_stocks():
    return update_yh_stocks()
