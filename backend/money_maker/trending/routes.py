import sqlalchemy
from flask import jsonify, Blueprint
from sqlalchemy import select, text, func, cast

from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice as tP

trending_bp = Blueprint('trending_bp', __name__)


@trending_bp.route("/trending/<exchange>-<market_cap>-<order>")
def ticker_information(exchange, market_cap, order):
    stmt: select = select(tP.symbol, tP.market_change_percentage, tP.market_cap,
                          cast(func.timezone('AESST', cast(tP.last_updated, sqlalchemy.TIME)), sqlalchemy.Text))\
        .where(tP.market_change_percentage.isnot(None))\
        .where(tP.market_cap > market_cap)\
        .where(tP.exchange == exchange)\
        .order_by(text(f"{tP.market_change_percentage.name} {order}"))\
        .limit(10)

    # noinspection PyProtectedMember
    return jsonify([element._asdict() for element in db.session.execute(stmt).all()])
