import pytest
from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, REPEAT_TESTS
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio

NUMBER_OF_PORTFOLIOS = 5
NUMBER_OF_STOCKS = 10


@pytest.mark.repeat(REPEAT_TESTS)
def test_get_all_portfolios(flask_application: FlaskClient, user_account_logged_in: dict,
                            user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN a user with a new portfolio name
    WHEN a user is logged in and wants to create a new portfolio
    THEN check that all portfolios are returned for the user

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
        sample_portfolio: The name of the sample portfolio
    """

    for pf in range(1, NUMBER_OF_PORTFOLIOS):
        response = flask_application.post(f"""/portfolio/{user_id}/other_pf_{pf}""")
        assert response.status_code == HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio).all()) == NUMBER_OF_PORTFOLIOS

    db.session.query(Portfolio).filter(Portfolio.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()

    assert len(db.session.query(Portfolio.user_id == user_id).all()) == 0


@pytest.mark.repeat(REPEAT_TESTS)
def test_get_all_stocks_from_portfolios(flask_application: FlaskClient, user_account_logged_in: dict,
                                        user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN a user with a portfolio
    WHEN a user is logged in, created a portfolio with stocks in it
    THEN check that stocks are returned from it

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
        sample_portfolio: The name of the sample portfolio
    """

    for i in range(1, NUMBER_OF_STOCKS + 1):
        response = flask_application.post(f"""/portfolio/{user_id}/{sample_portfolio}/{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == "Successfully added stock"

    response = flask_application.get(f"""/portfolio/{user_id}/{sample_portfolio}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(response.get_json()) == NUMBER_OF_STOCKS

    db.session.query(Portfolio).filter(Portfolio.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()

    assert len(db.session.query(Portfolio.user_id == user_id).all()) == 0
