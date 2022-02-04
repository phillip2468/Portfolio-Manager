from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio as pF, portfolio_schema

portfolio_bp = Blueprint("portfolio_bp", __name__, url_prefix="/portfolio")


@portfolio_bp.route("<user_id>", methods=["GET"])
def get_portfolio_names_by_user(user_id: int):
    """
    Returns all the portfolio names that a particular user
    has.
    :param user_id: The user id
    :return: flask.Response
    """
    results = db.session.query(pF.portfolio_name).filter(pF.user_id == user_id).all()
    return portfolio_schema.jsonify(results, many=True)


@portfolio_bp.route("<user_id>/<portfolio_name>", methods=["GET"])
def get_portfolio_stocks_by_user(user_id: int, portfolio_name: str):
    """
    Returns a stocks list by portfolio name.

    :param user_id: The user id
    :param portfolio_name: The portfolio name
    :return: flask.Response
    """
    results = db.session.query(pF.portfolio_name, pF.stock_id) \
        .filter(pF.user_id == user_id, pF.portfolio_name == portfolio_name).all()
    return portfolio_schema.jsonify(results, many=True)


@portfolio_bp.route("<user_id>/<portfolio_name>/<stock_id>", methods=["POST"])
def add_stock_to_portfolio(user_id: int, portfolio_name: str, stock_id: int):
    """
    Add a stock to a particular portfolio, using their stock_id from the database.
    Returns a message indicating user success.

    :param user_id: The user id
    :param portfolio_name: The portfolio name
    :param stock_id: The stock id
    :return: flask.Response
    """
    stock = pF(stock_id=stock_id, portfolio_name=portfolio_name, user_id=user_id)
    db.session.add(stock)
    db.session.commit()

    return jsonify({"msg", "Successfully added stock"}), 200


@portfolio_bp.errorhandler(IntegrityError)
def exception_handler(e):
    return jsonify({'message': e.description}), 400
