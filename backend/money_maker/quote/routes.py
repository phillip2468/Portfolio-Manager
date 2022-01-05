from flask import jsonify, Blueprint
from sqlalchemy import select

from money_maker.extensions import db
from money_maker.helpers import object_as_dict
from money_maker.models.ticker_prices import TickerPrice

quote_bp = Blueprint('quote_bp', __name__)


@quote_bp.route("/quote/<ticker>")
def ticker_information(ticker):
    stmt: select = select(TickerPrice).filter(TickerPrice.symbol == ticker)
    return jsonify([object_as_dict(element) for element in db.session.execute(stmt).one()])
