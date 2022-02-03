from flask_marshmallow import Schema
from money_maker.extensions import db, marshmallow
from sqlalchemy import (TIMESTAMP, Column, ForeignKey, ForeignKeyConstraint,
                        Integer, String, func)


class Portfolio(db.Model):
    """
    description: stores the portfolio information of
    each user's stocks in the database
    """
    __tablename__ = 'portfolio'
    portfolio_id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_name = Column(String(length=100), unique=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    stock_id = Column(Integer, ForeignKey('ticker_prices.stock_id'))
    last_inserted = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.utc_timestamp())
    ___table_args__ = (
        ForeignKeyConstraint(columns=["portfolio_name", "user_id", "stock_id"],
                             refcolumns=["portfolio_name", "user.user_id", "ticker_price.stock_id"],
                             onupdate="CASCADE", ondelete="CASCADE",), {}
    )


class PortfolioSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Portfolio


portfolio_schema: Schema = PortfolioSchema()
