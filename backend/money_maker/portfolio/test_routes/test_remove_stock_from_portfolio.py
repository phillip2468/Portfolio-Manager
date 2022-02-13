import pytest
from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, REPEAT_TESTS
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio

NUMBER_OF_STOCKS = 10


@pytest.mark.repeat(REPEAT_TESTS)
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
    assert response.get_json()["msg"] == "Successfully added stock"

    response = flask_application.delete(f"""/portfolio/{user_id}/{sample_portfolio}/1""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == "Successfully deleted the stock"

    # Remember that the empty portfolio still exists in the database
    assert len(db.session.query(Portfolio.user_id == user_id).all()) == 1
