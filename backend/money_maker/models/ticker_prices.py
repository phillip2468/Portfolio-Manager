# coding: utf-8

from money_maker.extensions import db


class TickerPrice(db.Model):
    __tablename__ = 'ticker_prices'

    stock_id = db.Column(db.Integer, primary_key=True, unique=True,
                         server_default=db.text("nextval('ticker_prices_stock_id_seq'::regclass)"))
    currency = db.Column(db.String(6))
    exchange = db.Column(db.String(10))
    stock_name = db.Column(db.String(150))
    market_cap = db.Column(db.BigInteger)
    market_state = db.Column(db.String(20))
    quote_type = db.Column(db.String(10))
    market_change = db.Column(db.Float(53))
    market_change_percentage = db.Column(db.Float(53))
    market_high = db.Column(db.Numeric)
    market_low = db.Column(db.Numeric)
    market_open = db.Column(db.Numeric)
    market_previous_close = db.Column(db.Numeric)
    market_current_price = db.Column(db.Numeric)
    market_volume = db.Column(db.BigInteger)
    last_updated = db.Column(db.DateTime(True), nullable=False, server_default="now()")
    symbol = db.Column(db.String(10), unique=True)
