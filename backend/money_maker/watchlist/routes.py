import flask
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required

from money_maker.extensions import db
from money_maker.helpers import verify_user
from money_maker.models.ticker_prices import TickerPrice as tP
from money_maker.models.watchlist import Watchlist as wL, watchlist_schema

watchlist_bp = Blueprint("watchlist_bp", __name__, url_prefix="/watchlist")


@watchlist_bp.route("<user_id>", methods=["GET"])
@jwt_required()
@verify_user
def get_watchlist_names_by_user(user_id: int) -> flask.Response:
    """
    Returns all the watchlists names that a particular user has.

    Args:
        user_id: The user id

    Returns:
        A response message containing a list of dictionaries of watchlist names.
    """
    results = db.session.query(wL.watchlist_name).distinct(wL.watchlist_name).filter(wL.user_id == user_id).all()
    return watchlist_schema.jsonify(results, many=True)


@watchlist_bp.route("<user_id>/<watchlist_name>", methods=["GET"])
@jwt_required()
@verify_user
def get_watchlist_stocks_by_user(user_id: int, watchlist_name: str):
    """
    Returns all stocks related to a particular watchlists.

    Args:
        user_id: The user id
        watchlist_name: The watchlist name

    Returns:
        A response message containing a list of dictionaries of watchlist stocks.
    """
    results = db.session.query(wL).filter(wL.user_id == user_id, wL.watchlist_name == watchlist_name).join(tP).all()
    return watchlist_schema.jsonify(results, many=True)


@watchlist_bp.route("<user_id>/<watchlist_name>", methods=["POST"])
@jwt_required()
@verify_user
def add_watchlist(user_id: int, watchlist_name: str) -> flask.Response:
    """
    Creates a new watchlist for the particular user. All watchlists start
    with no stocks.

    Args:
        user_id: The user id
        watchlist_name: The watchlist name

    Returns:
        A flask response containing a success message.

    """
    wl_data = {
        "watchlist_name": watchlist_name,
        "user_id": user_id
    }
    new_wl = watchlist_schema.load(wl_data)
    db.session.add(new_wl)
    db.session.commit()
    return make_response(jsonify({"msg": "Successfully created a new watchlist"}), 200)


@watchlist_bp.route("<user_id>/<watchlist_name>", methods=["DELETE"])
@jwt_required()
@verify_user
def remove_watchlist(user_id: int, watchlist_name: str) -> flask.Response:
    """
    Removes a watchlist for a particular user. Will not return any error
    messages if this watchlist does not exist.

    Args:
        user_id: The user id
        watchlist_name: The watchlist name

    Returns:
        A flask response containing a success message.

    """
    db.session.query(wL).filter(wL.user_id == user_id,
                                wL.watchlist_name == watchlist_name).delete(synchronize_session="fetch")
    db.session.commit()

    return make_response(jsonify({"msg": "Successfully removed the watchlist"}), 200)


@watchlist_bp.route("<user_id>/<watchlist_name>", methods=["PATCH"])
@jwt_required()
@verify_user
def update_watchlist_name(user_id: int, watchlist_name: str) -> flask.Response:
    """
    Update a watchlist's name by a user. Note that the new name for the watchlist
    must be sent within the body of the request.

    Args:
        user_id: The user id as an integer
        watchlist_name: The portfolio name as a string

    Returns:
        A flask response indicating success.

    """
    req = request.get_json(force=True)
    new_wl_name = req.get("watchlist_name", None)

    if len(new_wl_name) < 1:
        return make_response(jsonify(msg="Watchlist names can't be empty"), 400)

    db.session.query(wL).filter(wL.user_id == user_id, wL.watchlist_name == watchlist_name) \
        .update({"watchlist_name": new_wl_name}, synchronize_session="fetch")
    db.session.commit()
    return make_response(jsonify(msg="Successfully updated the watchlist name"), 200)


@watchlist_bp.route("<user_id>/<watchlist_name>/<stock_id>", methods=["POST"])
@jwt_required()
@verify_user
def add_stock_to_watchlist(user_id: int, watchlist_name: str, stock_id: int):
    """
    Add a stock to a particular watchlist, using their stock_id from the database.
    Returns a message indicating user success.

    :param user_id: The user id
    :param watchlist_name: The watchlist name
    :param stock_id: The stock id
    :return: flask.Response
    """
    stock = wL(stock_id=stock_id, watchlist_name=watchlist_name, user_id=user_id)
    db.session.add(stock)
    db.session.commit()

    return jsonify({"msg":  "Successfully added stock to the watchlist"}), 200


@watchlist_bp.route("<user_id>/<watchlist_name>/<stock_id>", methods=["DELETE"])
@jwt_required()
@verify_user
def remove_stock_from_watchlist(user_id: int, watchlist_name: str, stock_id: int):
    """
    Removes a particular stock from a users watchlist, using their stock_id from the database.
    Returns a message indicating user success.

    :param user_id: The user id
    :param watchlist_name: The watchlist name
    :param stock_id: The stock id
    :return: flask.Response
    """
    db.session.query(wL).filter(wL.stock_id == stock_id, wL.watchlist_name == watchlist_name, wL.user_id == user_id).delete()
    db.session.commit()

    return jsonify({"msg": "Successfully deleted the stock from the watchlist"}), 200

