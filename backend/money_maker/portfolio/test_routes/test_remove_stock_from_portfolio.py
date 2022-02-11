from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio


def test_remove_stock_from_portfolio(client, client_accounts, symbols, stock_prices, logged_in_user_id):
    """
    GIVEN a stock id
    WHEN a user is logged in and wants to remove a stock from a portfolio
    THEN check that the new stock has been removed

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

    response = client.delete(f"""/portfolio/{logged_in_user_id}/sample_portfolio/1""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(db.session.query(Portfolio).filter(Portfolio.stock_id == 1).all()) == 0
