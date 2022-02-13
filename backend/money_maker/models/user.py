import re

from flask_marshmallow import Schema
from money_maker.extensions import bcrypt, db, marshmallow
from sqlalchemy import TIMESTAMP, Column, Integer, Text, func
from sqlalchemy.orm import validates

# This model inspired by below link
# https://flask-praetorian.readthedocs.io/en/latest/notes.html#requirements-for-the-user-class


email_regex = r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'


class User(db.Model):
    """
    description: all the users in the database
    """
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Text, unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    last_signed_in = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.utc_timestamp(), nullable=False)
    portfolios = db.relationship('Portfolio', backref='user')

    @validates('email')
    def validate_email(self, key, email):
        pattern = re.compile(email_regex)
        if not bool(pattern.search(email)):
            raise ValueError("Invalid email")
        return email

    @validates('hashed_password')
    def validate_password(self, key, password):
        pattern = re.compile(password_regex)
        if not bool(pattern.search(password)):
            raise ValueError("Invalid password")
        return bcrypt.generate_password_hash(password).decode("utf-8")


class UserSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        include_relationships = True


users_schema: Schema = UserSchema()
