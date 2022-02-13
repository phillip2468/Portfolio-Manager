from functools import wraps

from flask import make_response
from flask_jwt_extended import get_jwt
from sqlalchemy import inspect


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def verify_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        identity_in_jwt = int(get_jwt()["sub"])
        identity_in_request = int(kwargs["user_id"])

        if identity_in_jwt != identity_in_request:
            return make_response({"error": "not a valid user"}, 400)

        return f(*args, **kwargs)

    return decorated
