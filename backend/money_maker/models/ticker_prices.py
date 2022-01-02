# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, Numeric, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TickerPrice(Base):
    __tablename__ = 'ticker_prices'

    stock_id = Column(Integer, primary_key=True, unique=True, server_default=text("nextval('ticker_prices_stock_id_seq'::regclass)"))
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
    last_updated = Column(DateTime(True), nullable=False, server_default=text("now()"))
    symbol = Column(String(10), unique=True)
