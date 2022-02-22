from decimal import Decimal

from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice, ticker_price_schema

invalid_stock_symbol = "JMNDKLADSAMJKDJMKASDJKMNA12312"


def test_get_stock_info(flask_application: FlaskClient) -> None:
    """
    GIVEN a request to check stock information
    WHEN requested this informaiton
    THEN check that the response is successful and that the symbols match
    in the database

    Note that we must convert the object from the backend to a normal JSON dictionary,
    since JSON has no idea what a decimal is.

    Args:
        flask_application: The flask application
    """
    list_of_stocks = db.session.query(TickerPrice).all()
    for stock in list_of_stocks:
        response = flask_application.get(f"""/quote/{stock.symbol}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        ticker_as_dictionary = {}
        for key, value in ticker_price_schema.dump(stock).items():
            if isinstance(value, Decimal):
                ticker_as_dictionary[key] = str(value)
            else:
                ticker_as_dictionary[key] = value
        assert response.get_json() == ticker_as_dictionary


def test_invalid_stock_info_from_database(flask_application: FlaskClient) -> None:
    """
    GIVEN a request to check stock information
    WHEN an invalid stock symbol is entered
    THEN check that the response is not successful and is rejected

    Args:
        flask_application: The flask application
    """
    response = flask_application.get(f"""/quote/{invalid_stock_symbol}""")
    assert response.status_code != HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == "Invalid stock symbol"
