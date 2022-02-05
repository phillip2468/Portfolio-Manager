from flask import Blueprint, jsonify, request
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio as pF
from money_maker.models.portfolio import portfolio_schema
from money_maker.models.ticker_prices import TickerPrice as tP
from sqlalchemy import distinct
from sqlalchemy.exc import IntegrityError

portfolio_bp = Blueprint("portfolio_bp", __name__, url_prefix="/portfolio")


@portfolio_bp.route("<user_id>", methods=["GET"])
def get_portfolio_names_by_user(user_id: int):
    """
    Returns all the portfolio names that a particular user
    has.
    :param user_id: The user id
    :return: flask.Response
    """
    results = db.session.query(pF.portfolio_name).distinct(pF.portfolio_name).filter(pF.user_id == user_id).all()
    return portfolio_schema.jsonify(results, many=True)


@portfolio_bp.route("<user_id>/<portfolio_name>", methods=["GET"])
def get_portfolio_stocks_by_user(user_id: int, portfolio_name: str):
    """
    Returns all the stocks that are under the particular portfolio name.

    :param user_id: The user id
    :param portfolio_name: The portfolio name
    :return: flask.Response
    """
    results = db.session.query(pF).filter(pF.user_id == user_id, pF.portfolio_name == portfolio_name).join(tP).all()
    return portfolio_schema.jsonify(results, many=True)


@portfolio_bp.route("<user_id>/<portfolio_name>", methods=["POST"])
def add_new_portfolio(user_id: int, portfolio_name: str):
    """
    Creates a new portfolio for the particular user. All portfolios start
    with no stocks.
    :param user_id: The user id
    :param portfolio_name: The portfolio name
    :return: flask.Response
    """

    new_portfilio = pF(portfolio_name=portfolio_name, user_id=user_id)
    db.session.add(new_portfilio)
    return jsonify({"msg", "Successfully created a new portfolio"}), 200


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


@portfolio_bp.route("<user_id>/<portfolio_name>/<stock_id>", methods=["PATCH"])
def add_stock_to_portfolio(user_id: int, portfolio_name: str, stock_id: int):
    """
    Updates a stock in a portfolio. The attributes that can be changed
    are the units_purchased or units_price attributes.

    :param user_id: The user id
    :param portfolio_name: The portfolio name
    :param stock_id: The stock id
    :return: flask.Response
    """
    req = request.get_json(force=True)
    units_price = req.get("units_price", None)
    units_purchased = req.get("units_purchased", None)

    db.session.query(pF).filter(pF.user_id == user_id, pF.portfolio_name == portfolio_name, pF.stock_id == stock_id)\
        .update({pF.units_price: units_price, pF.units_purchased: units_purchased}, synchronize_session="fetch")
    db.session.commit()

    return jsonify({"msg", "Successfully updated the stock"}), 200


@portfolio_bp.errorhandler(IntegrityError)
def exception_handler(e):
    return jsonify({'message': e.description}), 400
