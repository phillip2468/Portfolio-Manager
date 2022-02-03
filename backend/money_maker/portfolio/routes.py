from flask import Blueprint
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio, portfolio_schema

portfolio_bp = Blueprint("portfolio_bp", __name__, url_prefix="/portfolio")


@portfolio_bp.route("<user_id>", methods=["GET"])
def get_portfolio(user_id):
    results = db.session.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    return portfolio_schema.jsonify(results, many=True)
