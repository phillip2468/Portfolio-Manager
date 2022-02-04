from flask_marshmallow import Schema
from money_maker.extensions import db, marshmallow
from sqlalchemy import (TIMESTAMP, Column, ForeignKey,
                        Integer, String, func, UniqueConstraint)


class Watchlist(db.Model):
    """
    description: stores a watchlist of stocks by user.
    """
    __tablename__ = 'watchlist'
    watchlist_id = Column(Integer, primary_key=True, autoincrement=True)
    watchlist_name = Column(String(length=100), unique=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    stock_id = Column(Integer, ForeignKey('ticker_prices.stock_id'))
    last_inserted = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.utc_timestamp())
    ___table_args__ = (
        UniqueConstraint(watchlist_name, user_id, stock_id,
                         name="unique_stock_in_watchlist_by_user"),
    )


class WatchlistSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Watchlist


portfolio_schema: Schema = WatchlistSchema()
