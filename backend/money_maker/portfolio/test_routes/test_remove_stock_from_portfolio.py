import pytest
from conftest import (ADD_STOCK_TO_PORTFOLIO, CREATE_PORTFOLIO_MSG,
                      DELETE_STOCK_TO_PORTFOLIO, HTTP_SUCCESS_CODE,
                      LOGIN_SUCCESS_MSG)
from flask.testing import FlaskClient
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio

NUMBER_OF_STOCKS = 10


def test_remove_stock_from_portfolio(flask_application: FlaskClient, user_account_logged_in: dict,
                                     user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN a stock id
    WHEN a user is logged in and wants to remove a stock from a portfolio
    THEN check that the new stock has been removed

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
        sample_portfolio: The name of the sample portfolio
    """
    response = flask_application.post(f"""/portfolio/{user_id}/{sample_portfolio}/1""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == ADD_STOCK_TO_PORTFOLIO

    response = flask_application.delete(f"""/portfolio/{user_id}/{sample_portfolio}/1""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == DELETE_STOCK_TO_PORTFOLIO

    # Remember that the empty portfolio still exists in the database
    assert len(db.session.query(Portfolio.user_id == user_id).all()) == 1


def test_invalid_remove_stock_from_portfolio(flask_application: FlaskClient, user_accounts: list[dict]) -> None:
    """
    GIVEN a stock id
    WHEN another user deletes a stock from a portfolio
    THEN check that the new stock has NOT been removed

    Args:
        flask_application: The flask application
        user_accounts: The list of dictionaries of registered users
    """
    response = flask_application.post("/auth/login", json=user_accounts[0])
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == LOGIN_SUCCESS_MSG

    response = flask_application.get("/auth/which_user")
    assert response.status_code == HTTP_SUCCESS_CODE
    user_id = response.get_json()["user_id"]

    response = flask_application.post(f"""/portfolio/{user_id}/sample_portfolio""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == CREATE_PORTFOLIO_MSG

    response = flask_application.post(f"""/portfolio/{user_id}/sample_portfolio/1""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == ADD_STOCK_TO_PORTFOLIO

    response = flask_application.post("/auth/login", json=user_accounts[1])
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == LOGIN_SUCCESS_MSG

    response = flask_application.delete(f"""/portfolio/{user_id}/sample_portfolio/1""")
    assert response.status_code != HTTP_SUCCESS_CODE

    # Remember that the empty portfolio still exists in the database
    assert len(db.session.query(Portfolio.user_id == user_id).all()) == 2

    db.session.query(Portfolio).filter(Portfolio.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()
