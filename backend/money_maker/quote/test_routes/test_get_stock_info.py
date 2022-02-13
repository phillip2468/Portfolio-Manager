import pytest
from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, REPEAT_TESTS
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice


@pytest.mark.repeat(REPEAT_TESTS)
def test_remove_stock_from_portfolio(flask_application: FlaskClient, user_account_logged_in: dict,
                                     user_id: int) -> None:
    """
    GIVEN a request to check stock information
    WHEN requested this informaiton
    THEN check that the response is successful and that the symbols match
    in the database

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
    """
    list_of_stocks = db.session.query(TickerPrice).all()
    for stock in list_of_stocks:
        request = flask_application.get(f"""/quote/{stock.symbol}""")
        assert request.status_code == HTTP_SUCCESS_CODE
        assert request.get_json()["symbol"] == stock.symbol


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_stock_info_from_database(flask_application: FlaskClient, user_account_logged_in: dict,
                                          user_id: int):
    """
    GIVEN a request to check stock information
    WHEN an invalid stock symbol is entered
    THEN check that the response is not successful and is rejected

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
    """
    response = flask_application.get(f"""/quote/JMNDKLADSAMJKDJMKASDJKMNA12312""")
    assert response.status_code != HTTP_SUCCESS_CODE
    assert response.get_json()["error"] == "Invalid stock symbol"
    
