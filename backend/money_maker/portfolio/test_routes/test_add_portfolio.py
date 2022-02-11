import pytest
from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, REPEAT_TESTS


@pytest.mark.repeat(REPEAT_TESTS)
def test_add_portfolio(client: FlaskClient, client_accounts: list[dict],
                       symbols: None, stock_prices: None, logged_in_user_id: int) -> None:
    """
    GIVEN a portfolio name
    WHEN a user is logged in and wants to create a portfolio
    THEN check that the new portfolio has been created.
    Args:
        client: The flask app
        client_accounts: List of dict
        symbols: Places symbols into database TickerPrice
        stock_prices: Places stock prices into database TickerPrice
        logged_in_user_id: The user id logged in
    """
    response = client.post(f"""/portfolio/{logged_in_user_id}/sample_portfolio""")
    assert response.status_code == HTTP_SUCCESS_CODE


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_portfolio_name(client: FlaskClient, client_accounts: list[dict], symbols: None,
                                stock_prices: None, logged_in_user_id: int) -> None:
    """
    GIVEN a portfolio name which is empty
    WHEN a user is logged in and wants to create a portfolio
    THEN check the portfolio is not created

    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients
        symbols: The query to create stock symbol rows
        stock_prices: The query to update up to 100 stocks of alphabetically
        logged_in_user_id: The logged-in user_id

    """
    response = client.post(f"""/portfolio/{logged_in_user_id}/""")
    assert response.status_code != HTTP_SUCCESS_CODE
