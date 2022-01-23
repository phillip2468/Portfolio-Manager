from flask import Blueprint, jsonify, request
from money_maker.extensions import praetorian

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"email":"Walter","password":"calmerthanyouare"}'
    """
    req = request.get_json(force=True)
    print(req)
    email = req.get("email", None)
    password = req.get("password", None)
    user = praetorian.authenticate(email, password)
    ret = {"access_token": praetorian.encode_jwt_token(user)}
    return jsonify(ret), 200
