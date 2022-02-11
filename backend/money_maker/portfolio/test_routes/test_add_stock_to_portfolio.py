from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio


def test_add_stock_to_portfolio(client, client_accounts, symbols, stock_prices, logged_in_user_id):
    """
    GIVEN a stock id
    WHEN a user is logged in and wants to add a stock to portfolio
    THEN check that the new stock has been added

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

    response = client.post(f"""/portfolio/{logged_in_user_id}/sample_portfolio/1""")
    assert response.status_code == HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio)
               .filter(Portfolio.user_id == logged_in_user_id, Portfolio.stock_id == 1).all()) == 1


def test_add_multiple_stocks_to_portfolio(client, client_accounts, symbols, stock_prices, logged_in_user_id):
    """
    GIVEN multiple stock_ids
    WHEN a user is logged in and wants to add a stock to portfolio
    THEN check that the new stock has been added

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

    for i in range(1, 9):
        response = client.post(f"""/portfolio/{logged_in_user_id}/sample_portfolio/{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == logged_in_user_id).all()) == 9


def test_add_multiple_stocks_to_different_portfolios(client, client_accounts, symbols, stock_prices, logged_in_user_id):
    """
    GIVEN multiple stock_ids
    WHEN a user is logged in and wants to add a stock to a particular portfolio (and already has multiple portfolios)
    THEN check that the new stock has been added to the right portfolio

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

    response = client.post(f"""/portfolio/{logged_in_user_id}/sample_portfolio_2""")
    assert response.status_code == HTTP_SUCCESS_CODE

    for i in range(1, 9):
        response = client.post(f"""/portfolio/{logged_in_user_id}/sample_portfolio/{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == logged_in_user_id).all()) == 10


def test_add_invalid_stock_to_portfolio(client, client_accounts, symbols, stock_prices, logged_in_user_id):
    """
    GIVEN an invalid stock_id
    WHEN a user is logged in and wants to add a stock to a particular portfolio
    THEN check that the new stock has not been added

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

    response = client.post(f"""/portfolio/{logged_in_user_id}/sample_portfolio/-100""")
    assert response.status_code != HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio.stock_id)
               .filter(Portfolio.user_id == logged_in_user_id, Portfolio.stock_id == -100).all()) == 0
