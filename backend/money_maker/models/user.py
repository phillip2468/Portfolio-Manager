from marshmallow import Schema
from money_maker.extensions import db, marshmallow
from sqlalchemy import TIMESTAMP, Column, Integer, Text, func

# This model inspired by below link
# https://flask-praetorian.readthedocs.io/en/latest/notes.html#requirements-for-the-user-class


class User(db.Model):
    """
    description: all the users in the database
    """
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Text, unique=True)
    hashed_password = Column(Text)
    last_signed_in = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.utc_timestamp())


class UserSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = User


users_schema: Schema = UserSchema()
