from flask_marshmallow import Schema
from marshmallow import fields
from money_maker.extensions import db, marshmallow
from money_maker.models.ticker_prices import TickerPriceSchema
from sqlalchemy import (DATE, TIMESTAMP, Column, ForeignKey, Integer, Numeric,
                        String, UniqueConstraint, func)
from sqlalchemy.orm import relationship, validates


class Portfolio(db.Model):
    """
    description: stores the portfolio information of
    each user's stocks in the database. Note that this table differs
    from watchlist by being able simulating what an actual stock
    portfolio has by having stock purchase prices.
    """
    __tablename__ = 'portfolio'
    portfolio_id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_name = Column(String(length=100))
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    stock_id = Column(Integer, ForeignKey('ticker_prices.stock_id'))
    units_purchased = Column(Integer)
    units_price = Column(Numeric)
    date_purchased = Column(DATE)
    last_inserted = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.utc_timestamp())
    stock_details = relationship("TickerPrice", backref="portfolio")
    ___table_args__ = (
        UniqueConstraint(portfolio_name, user_id, stock_id,
                         name="unique_stock_in_portfolio_by_user"),
    )

    @validates('portfolio_name')
    def validate_portfolio_name(self, key, portfolio_name):
        if len(portfolio_name) < 1:
            raise ValueError("Invalid portfolio name")
        return portfolio_name


class PortfolioSchema(marshmallow.SQLAlchemyAutoSchema):
    stock_details = fields.Nested(TickerPriceSchema)

    class Meta:
        model = Portfolio
        load_instance = True
        include_fk = True
        include_relationships = True


portfolio_schema: marshmallow.Schema = PortfolioSchema()

