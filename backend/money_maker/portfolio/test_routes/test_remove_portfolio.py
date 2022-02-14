from conftest import (HTTP_SUCCESS_CODE, LOGIN_SUCCESS_MSG,
                      NEW_PORTFOLIO_SUCCESS_MSG)
from flask.testing import FlaskClient
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio


def test_remove_portfolio(flask_application: FlaskClient, user_account_logged_in: dict, user_id: int) -> None:
    """
    GIVEN a user that has a portfolio
    WHEN a user wants to remove this portfolio
    THEN check that the portfolio is removed

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
    """

    response = flask_application.post(f"""/portfolio/{user_id}/sample_portfolio""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == "Successfully created a new portfolio"

    response = flask_application.delete(f"""/portfolio/{user_id}/sample_portfolio""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == "Successfully deleted the portfolio"

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id).all()) == 0


def test_invalid_remove_other_user_portfolio(flask_application: FlaskClient, user_accounts: list[dict]) -> None:
    """
    GIVEN a user that has a portfolio
    WHEN a user wants to remove this portfolio
    THEN check that the portfolio is removed

    Args:
        flask_application: The flask application
        user_accounts: The list of dictionaries of other registered users.
    """
    response = flask_application.post("/auth/login", json=user_accounts[0])
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == LOGIN_SUCCESS_MSG

    response = flask_application.get("auth/which_user")
    assert response.status_code == HTTP_SUCCESS_CODE
    user_id = response.get_json()["user_id"]

    response = flask_application.post(f"""/portfolio/{user_id}/sample_portfolio""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == NEW_PORTFOLIO_SUCCESS_MSG

    response = flask_application.post("/auth/login", json=user_accounts[1])
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == LOGIN_SUCCESS_MSG

    response = flask_application.delete(f"""/portfolio/{user_id}/sample_portfolio""")
    assert response.status_code != HTTP_SUCCESS_CODE

    db.session.query(Portfolio).filter(Portfolio.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()
    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id).all()) == 0
