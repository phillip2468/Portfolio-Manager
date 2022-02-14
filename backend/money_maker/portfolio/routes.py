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
@jwt_required()
@verify_user
def get_portfolio_names_by_user(user_id: int) -> flask.Response:
    """
    Returns all portfolio names belonging to a particular user
    that is logged in.

    Args:
        user_id (int): The user id

    Returns:
        The flask response as a list of dictionaries of Portfolio objects.
    """
    results = db.session.query(pF.portfolio_name).distinct(pF.portfolio_name).filter(pF.user_id == user_id).all()
    return portfolio_schema.jsonify(results, many=True)


@portfolio_bp.route("<user_id>/<portfolio_name>", methods=["GET"])
@jwt_required()
@verify_user
def get_portfolio_stocks_by_user(user_id: int, portfolio_name: str) -> flask.Response:
    """
    Returns all stocks details from a particular portfolio name
    belonging to a particular user.

    Args:
        user_id (int): The user id
        portfolio_name (): The portfolio name of the user.

    Returns:
        The flask response as a list of portfolio objects,
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
        user_id: The user id
        portfolio_name: The portfolio name

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


@portfolio_bp.route("<user_id>/<portfolio_name>", methods=["DELETE"])
@jwt_required()
@verify_user
def remove_portfolio(user_id: int, portfolio_name: str) -> Response:
    """
    Remove an entire portfolio from a user, using their user_id, portfolio_name.
    Returns a message indicating user success. Note that portfolios that don't exist will not return
    any error messages.

    Args:
        user_id: The user id as an integer
        portfolio_name: The portfolio name as a string

    Returns:
        A flask response indicating success.

    """
    db.session.query(pF).filter(pF.user_id == user_id,
                                pF.portfolio_name == portfolio_name).delete(synchronize_session="fetch")
    db.session.commit()
    return make_response(jsonify(msg="Successfully deleted the portfolio"), 200)


@portfolio_bp.route("<user_id>/<portfolio_name>", methods=["PATCH"])
@jwt_required()
@verify_user
def update_portfolio_name(user_id: int, portfolio_name: str) -> Response:
    """
    Update a portfolio's name by a user. Note that the new name for the portfolio
    must be sent within the body of the request.

    Args:
        user_id: The user id as an integer
        portfolio_name: The portfolio name as a string

    Returns:
        A flask response indicating success.

    """
    req = request.get_json(force=True)
    new_pf_name = req.get("portfolio_name", None)

    if len(new_pf_name) < 1:
        return make_response(jsonify(msg="Portfolio names can't be empty"), 400)

    db.session.query(pF).filter(pF.user_id == user_id, pF.portfolio_name == portfolio_name)\
        .update({"portfolio_name": new_pf_name}, synchronize_session="fetch")
    db.session.commit()
    return make_response(jsonify(msg="Successfully updated the portfolio name"), 200)


@portfolio_bp.route("<user_id>/<portfolio_name>/<stock_id>", methods=["POST"])
@jwt_required()
@verify_user
def add_stock_to_portfolio(user_id: int, portfolio_name: str, stock_id: int) -> Response:
    """
    Add a stock to a particular portfolio, using their stock_id from the database.
    Returns a message indicating user success.

    If either the stock is not found in the database, or the portfolio entry does not exist
    returns a message indicating failure.

    Args:
        user_id: The user id
        portfolio_name: The portfolio name
        stock_id: The stock id

    Returns:
        A flask response indicating success.
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
@jwt_required()
@verify_user
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
@jwt_required()
@verify_user
def update_stock_in_portfolio(user_id: int, portfolio_name: str, stock_id: int) -> flask.Response:
    """
    Updates a stock in a portfolio. The attributes that can be changed
    are the units_purchased or units_price attributes. Note that the details
    to be updated must be within the body of the request.

    Args:
        user_id: The user id
        portfolio_name: The portfolio name
        stock_id: The stock id

    Returns:
        A message indicating the portofolio stock details have been updated
    """

    req = request.get_json(force=True)
    units_price = req.get("units_price", None)
    units_purchased = req.get("units_purchased", None)

    db.session.query(pF).filter(pF.user_id == user_id, pF.portfolio_name == portfolio_name, pF.stock_id == stock_id) \
        .update(values={"units_price": units_price, "units_purchased": units_purchased}, synchronize_session="fetch")
    db.session.commit()

    return make_response(jsonify(msg="Successfully updated the stock details"), 200)


@portfolio_bp.errorhandler(IntegrityError)
def exception_handler(e):
    return jsonify({'message': e}), 400
