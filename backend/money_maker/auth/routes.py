from flask import Blueprint, jsonify, request
from money_maker.extensions import jwt_manager, db, bcrypt
from money_maker.models.user import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    . example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"email":"Walter","password":"calmerthanyouare"}'
    """
    req = request.get_json(force=True)
    email = req.get("email", None)
    password = req.get("password", None)

    user: User = db.session.query(User).filter(User.email == email).one_or_none()

    if not email or not password or not user:
        return jsonify(error="Missing credentials"), 400

    if bcrypt.check_password_hash(user.hashed_password, password):
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify(error="Invalid login details"), 400


@auth_bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh_tokens():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=db.session.query(User).filter(User.user_id == identity).one())
    return jsonify(access_token=access_token)


@jwt_manager.user_identity_loader
def user_identity_lookup(user: User):
    """
    Register a callback function that takes whatever object is passed in as the
    identity when creating JWTs and converts it to a JSON serializable format.

    :param user:
    :return:
    """
    return user.user_id


@jwt_manager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
     Register a callback function that loads a user from your database whenever
     a protected route is accessed. This should return any python object on a
     successful lookup, or None if the lookup failed for any reason (for example
     if the user has been deleted from the database).

    :param _jwt_header:
    :param jwt_data:
    :return:
    """
    identity = jwt_data["sub"]
    return db.session.query(User).filter(User.user_id == identity).one_or_none()
