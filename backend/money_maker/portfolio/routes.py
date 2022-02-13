import flask
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from werkzeug.wrappers import Response

from money_maker.extensions import db
from money_maker.helpers import verify_user
from money_maker.models.portfolio import Portfolio
from money_maker.models.portfolio import Portfolio as pF
from money_maker.models.portfolio import portfolio_schema
from money_maker.models.ticker_prices import TickerPrice
from money_maker.models.ticker_prices import TickerPrice as tP

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
@jwt_required()
@verify_user
def create_new_portfolio(user_id: int, portfolio_name: str) -> flask.Response:
    """
    Creates a new portfolio for the particular user. All portfolios start
    with no stocks.
    Args:
        user_id (int): The user id
        portfolio_name (str): The portfolio name

    Returns:
    A response containing user success.
    """
    pf_data = {
        "portfolio_name": portfolio_name,
        "user_id": user_id
    }
    new_pf = portfolio_schema.load(pf_data)
    db.session.add(new_pf)
    db.session.commit()

    return make_response({"msg": "Successfully created a new portfolio"}, 200)



@portfolio_bp.route("<user_id>/<portfolio_name>/<stock_id>", methods=["POST"])
def add_stock_to_portfolio(user_id: int, portfolio_name: str, stock_id: int) -> Response:
    """
    Add a stock to a particular portfolio, using their stock_id from the database.
    Returns a message indicating user success.

    :param user_id: The user id
    :param portfolio_name: The portfolio name
    :param stock_id: The stock id
    :return: flask.Response
    """
    if len(db.session.query(TickerPrice).filter(TickerPrice.stock_id == stock_id).all()) == 0:
        return make_response(jsonify(msg="Stock not found"), 400)

    if (len(db.session.query(Portfolio)
                    .filter(Portfolio.portfolio_name == portfolio_name, Portfolio.user_id == user_id).all())) == 0:
        return make_response(jsonify(msg="Portfolio not found"), 400)

    stock = pF(stock_id=stock_id, portfolio_name=portfolio_name, user_id=user_id, units_price=0, units_purchased=0)
    db.session.add(stock)
    db.session.commit()

    return make_response(jsonify(msg="Successfully added stock"), 200)


@portfolio_bp.route("<user_id>/<portfolio_name>/<stock_id>", methods=["DELETE"])
def remove_stock_from_portfolio(user_id: int, portfolio_name: str, stock_id: int) -> Response:
    """
    Removes a particular stock from a user's portfolio, using their stock_id from the database.
    Returns a message indicating user success. Note that stock ids that don't exist WILL NOT raise any errors.

    Args:
        user_id: The user id as an integer
        portfolio_name: The portfolio name as a string
        stock_id: The stock id as written in the database.

    Returns:
        A flask response indicating success.

    """

    db.session.query(pF).filter(pF.stock_id == stock_id, pF.portfolio_name == portfolio_name,
                                pF.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()

    return make_response(jsonify(msg="Successfully deleted the stock"), 200)


@portfolio_bp.route("<user_id>/<portfolio_name>/<stock_id>", methods=["PATCH"])
def update_stock_in_portfolio(user_id: int, portfolio_name: str, stock_id: int):
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

    db.session.query(pF).filter(pF.user_id == user_id, pF.portfolio_name == portfolio_name, pF.stock_id == stock_id) \
        .update(values={"units_price": units_price, "units_purchased": units_purchased}, synchronize_session="fetch")
    db.session.commit()

    return jsonify({"msg": "Successfully updated the stock"}), 200


@portfolio_bp.errorhandler(IntegrityError)
def exception_handler(e):
    return jsonify({'message': e}), 400
