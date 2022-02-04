from flask_marshmallow import Schema
from money_maker.extensions import db, marshmallow
from sqlalchemy import (TIMESTAMP, Column, ForeignKey,
                        Integer, String, func, UniqueConstraint, Numeric, DATE)


class Portfolio(db.Model):
    """
    description: stores the portfolio information of
    each user's stocks in the database. Note that this table differs
    from watchlist by being able simulating what an actual stock
    portfolio has by having stock purchase prices.
    """
    __tablename__ = 'portfolio'
    portfolio_id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_name = Column(String(length=100), unique=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    stock_id = Column(Integer, ForeignKey('ticker_prices.stock_id'))
    units_purchased = Column(Integer)
    units_price = Column(Numeric)
    date_purchased = Column(DATE)
    last_inserted = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.utc_timestamp())
    ___table_args__ = (
        UniqueConstraint(portfolio_name, user_id, stock_id,
                         name="unique_stock_in_portfolio_by_user"),
    )


class PortfolioSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Portfolio


portfolio_schema: Schema = PortfolioSchema()
