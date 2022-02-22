from datetime import datetime, timedelta, timezone

import flask
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import (create_access_token, get_jwt, get_jwt_identity,
                                jwt_required, set_access_cookies,
                                unset_jwt_cookies)

from money_maker.extensions import bcrypt, db
from money_maker.models.user import User, users_schema

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


# https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/#implicit-refreshing-with-cookies
# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@auth_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@auth_bp.route("/login", methods=["POST"])
def login() -> flask.Response:
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token. First checks if the email exists and then verifies the password
    hash.

    Returns:
        A flask response indicating if the user was successful
    """
    req = request.get_json(force=True)
    email = req.get("email", None)
    password = req.get("password", None)

    user = db.session.query(User).filter(User.email == email).one_or_none()

    if not email or not password or not user:
        return make_response(jsonify(msg="Missing credentials or wrong login"), 400)

    if bcrypt.check_password_hash(user.hashed_password, password):
        response = jsonify({"msg": "login successful"})
        access_token = create_access_token(identity=user.user_id)
        set_access_cookies(response, access_token)
        return make_response(response, 200)
    else:
        return make_response(jsonify(msg="Invalid login details"), 400)


@auth_bp.route("/logout", methods=["POST"])
def logout() -> flask.Response:
    """
    Logs out a user from the frontend. Note that
    a jwt is not required as potentially jwt's may be expired
    or non-existant.

    Returns:
        A flask response indicating if the user was successful
    """
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@auth_bp.route("/register", methods=["POST"])
def register() -> flask.Response:
    """
    Registers a new user account with an email and password. Note that this
    route automatically validates correct user details with the database.

    Returns:
        A flask response indicating if the user was successful

    """
    req = request.get_json(force=True)
    email = req.get("email", None)
    password = req.get("password", None)

    try:
        new_user = User(email=email, hashed_password=password)
        db.session.add(new_user)
        db.session.commit()
    except ValueError:
        db.session.rollback()
        return make_response(jsonify({"msg": "Error with user details"}), 400)

    response = jsonify({"msg": "register successful"})
    access_token = create_access_token(identity=new_user.user_id)
    set_access_cookies(response, access_token)

    return make_response(response, 200)


@auth_bp.route("/which_user", methods=["GET"])
@jwt_required()
def which_user() -> flask.Response:
    """
    Using the cookie which contains the user_id of the particular user,
    check with the database to find out the indicated user.

    Returns:
        A flask response indicating if the user was successful
    """
    user = db.session.query(User.user_id).filter(User.user_id == get_jwt()["sub"]).one_or_none()
    if user is None:
        return make_response(jsonify({"msg": "Error finding user"}), 400)
    return users_schema.jsonify(user)

