import pytest
from conftest import HTTP_SUCCESS_CODE, REPEAT_TESTS


@pytest.mark.repeat(REPEAT_TESTS)
def test_add_portfolio(client, client_accounts, symbols, stock_prices, logged_in_user_id):
    """
    GIVEN a portfolio name
    WHEN a user is logged in and wants to create a portfolio
    THEN check that the new portfolio has been created.

    :param client: The flask testing client
    :type client: FlaskClient
    :param client_accounts: The users in the database
    :type client_accounts: dict
    :param symbols: The stock ticker symbols
    :type symbols: Any
    :param stock_prices: A fixture which updates all the stock prices from the symbol's fixture
    :type stock_prices: Any
    :param logged_in_user_id: The id of the user
    :type logged_in_user_id: int
    """
    response = client.post(f"""/portfolio/{logged_in_user_id}/sample_portfolio""")
    assert response.status_code == HTTP_SUCCESS_CODE


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_portfolio_name(client, client_accounts, symbols, stock_prices, logged_in_user_id):
    """
    GIVEN a portfolio name which is empty
    WHEN a user is logged in and wants to create a portfolio
    THEN check the portfolio is not created

    :param client: The flask testing client
    :type client: FlaskClient
    :param client_accounts: The users in the database
    :type client_accounts: dict
    :param symbols: The stock ticker symbols
    :type symbols: Any
    :param stock_prices: A fixture which updates all the stock prices from the symbol's fixture
    :type stock_prices: Any
    :param logged_in_user_id: The id of the user
    :type logged_in_user_id: int
    """
    response = client.post(f"""/portfolio/{logged_in_user_id}/""")
    assert response.status_code != HTTP_SUCCESS_CODE
