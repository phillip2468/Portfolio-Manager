from conftest import (CREATE_PORTFOLIO_MSG, DELETE_PORTFOLIO_MSG,
                      HTTP_SUCCESS_CODE)
from flask.testing import FlaskClient
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio


def test_update_portfolio_name(flask_application: FlaskClient, user_account_logged_in: dict, user_id: int) -> None:
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
    assert response.get_json()["msg"] == CREATE_PORTFOLIO_MSG

    response = flask_application.delete(f"""/portfolio/{user_id}/sample_portfolio""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == DELETE_PORTFOLIO_MSG

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id).all()) == 0

