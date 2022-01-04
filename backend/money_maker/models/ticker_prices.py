# coding: utf-8

from money_maker.extensions import db
from sqlalchemy.types import Integer, String, Numeric, DateTime, Float, BigInteger
from sqlalchemy import Column
from sqlalchemy.sql import func


class TickerPrice(db.Model):
    __tablename__ = 'ticker_prices'

    stock_id = Column(Integer, primary_key=True, autoincrement=True)
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
    last_updated = Column(DateTime(True), nullable=False, server_default=func.now())
    symbol = Column(String(10), unique=True)
