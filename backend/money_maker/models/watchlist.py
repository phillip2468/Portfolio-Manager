from flask_marshmallow import Schema
from marshmallow import fields
from money_maker.extensions import db, marshmallow
from money_maker.models.ticker_prices import TickerPriceSchema
from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Integer, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import relationship


class Watchlist(db.Model):
    """
    description: stores a watchlist of stocks by user.
    """
    __tablename__ = 'watchlist'
    watchlist_id = Column(Integer, primary_key=True, autoincrement=True)
    watchlist_name = Column(String(length=100))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    stock_id = Column(Integer, ForeignKey('ticker_prices.stock_id'))
    last_inserted = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.utc_timestamp())
    stock_details = relationship("TickerPrice", backref="watchlist")
    ___table_args__ = (
        UniqueConstraint(watchlist_name, user_id, stock_id,
                         name="unique_stock_in_watchlist_by_user"),
    )


class WatchlistSchema(marshmallow.SQLAlchemyAutoSchema):
    stock_details = fields.Nested(TickerPriceSchema)

    class Meta:
        model = Watchlist
        load_instance = True
        include_fk = True
        include_relationships = True


watchlist_schema: Schema = WatchlistSchema()

