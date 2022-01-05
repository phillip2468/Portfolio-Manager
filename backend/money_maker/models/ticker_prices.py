# coding: utf-8

from money_maker.extensions import db
from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.types import (TIMESTAMP, BigInteger, Float, Integer, Numeric,
                              String)


class TickerPrice(db.Model):
    __tablename__ = 'ticker_prices'

    stock_id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), unique=True)
    city = Column(String(20))
    country = Column(String(30))
    industry = Column(String(50))
    zip_code = Column(String(15))
    sector = Column(String(30))
    currency = Column(String(6))
    exchange = Column(String(10))
    stock_name = Column(String(150))
    market_cap = Column(BigInteger)
    market_state = Column(String(20))
    quote_type = Column(String(10))
    market_change = Column(Float(53))
    market_change_percentage = Column(Float(53))
    market_high = Column(Numeric)
    market_low = Column(Numeric)
    market_open = Column(Numeric)
    market_previous_close = Column(Numeric)
    market_current_price = Column(Numeric)
    market_volume = Column(BigInteger)
    last_updated = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.utc_timestamp())  # type: ignore
