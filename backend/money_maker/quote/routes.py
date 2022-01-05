from flask import Blueprint, jsonify
from money_maker.extensions import db
from money_maker.helpers import object_as_dict
from money_maker.models.ticker_prices import TickerPrice
from sqlalchemy import select

quote_bp = Blueprint('quote_bp', __name__)


@quote_bp.route("/quote/<ticker>")
def ticker_information(ticker):
    stmt: select = select(TickerPrice).filter(TickerPrice.symbol == ticker)
    return jsonify([object_as_dict(element) for element in db.session.execute(stmt).one()])
