from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE

example_period = "60d"
example_interval = "1d"
example_invalid_interval = "1m"
list_of_keys = ["open", "time"]
example_stock = "AAPL"


def test_valid_historical_data_by_symbol(flask_application: FlaskClient) -> None:
    """
    GIVEN a request to check stock information
    WHEN a valid stock symbol is entered
    THEN check that the response contains the historical data of the above stock.

    Args:
        flask_application: The flask application
    """
    response = flask_application.get(f"""/quote/{example_stock}&period={example_period}&interval={example_interval}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json() is not None
    assert response.get_json()["currency_symbol"] == "$"
    assert response.get_json()["price_now"] > 0
    list_of_prices = response.get_json()["priceList"]
    # noinspection PyShadowingNames
    assert all(list_of_keys in list_of_prices for list_of_keys in list_of_prices)


def test_invalid_stock_historical_data(flask_application: FlaskClient) -> None:
    """
    GIVEN a request to check stock information
    WHEN an invalid stock symbol is entered
    THEN check that the response does not return 200.

    Args:
        flask_application: The flask application
    """
    response = flask_application.get(f"""/quote/A1231231231PL&period={example_period}&interval={example_interval}""")
    assert response.status_code != HTTP_SUCCESS_CODE


def test_invalid_time_period_interval(flask_application: FlaskClient) -> None:
    """
    GIVEN a request to check historical pricing
    WHEN a valid stock symbol is entered but the time period or interval is too small or large (but still valid)
    THEN check that the response does not return 200.

    Args:
        flask_application: The flask application
    """
    response = flask_application.get(f"""/quote/{example_stock}&period={example_period}&interval={example_invalid_interval}""")
    assert response.status_code != HTTP_SUCCESS_CODE

