from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio


def test_get_all_portfolios(client, client_accounts, symbols, stock_prices, logged_in_user_id):
    """
    GIVEN a user id
    WHEN a user is logged in
    THEN check that all portfolios are returned for the user

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

    for i in range(1, 5):
        response = client.post(f"""/portfolio/{logged_in_user_id}/sample_portfolio{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio)
               .filter(Portfolio.user_id == logged_in_user_id).all()) > 1

    response = client.get(f"""/portfolio/{logged_in_user_id}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(response.get_json()) > 1


def test_get_all_stocks_from_portfolio(client, client_accounts, symbols, stock_prices, logged_in_user_id, sample_portfolio):
    """
    GIVEN a user id
    WHEN a user is logged in
    THEN check that all stocks from a portfolios are returned for the user

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

    assert len(db.session.query(Portfolio)
               .filter(Portfolio.user_id == logged_in_user_id).all()) == 1

    for i in range(1, 10):
        response = client.post(f"""/portfolio/{logged_in_user_id}/{sample_portfolio}/{i}""")
        assert response.status_code == 200

    response = client.get(f"""/portfolio/{logged_in_user_id}/{sample_portfolio}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(response.get_json()) == 9
