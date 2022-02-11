from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db, faker_data
from money_maker.models.portfolio import Portfolio


def test_add_stock_to_portfolio(client: FlaskClient, client_accounts: list[dict], symbols: None,
                                stock_prices: None, logged_in_user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN a stock id
    WHEN a user is logged in and wants to add a stock to portfolio
    THEN check that the new stock has been added
    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients
        symbols: The query to create stock symbol rows
        stock_prices: The query to update up to 100 stocks of alphabetically
        logged_in_user_id: The logged-in user_id
        sample_portfolio: Places sample portfolio into database portfolio
    """

    response = client.post(f"""/portfolio/{logged_in_user_id}/{sample_portfolio}/1""")
    assert response.status_code == HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio)
               .filter(Portfolio.user_id == logged_in_user_id, Portfolio.stock_id == 1).all()) == 1


def test_add_multiple_stocks_to_portfolio(client: FlaskClient, client_accounts: list[dict], symbols: None,
                                          stock_prices: None, logged_in_user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN multiple stock_ids
    WHEN a user is logged in and wants to add a stock to portfolio
    THEN check that the new stock has been added
    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients
        symbols: The query to create stock symbol rows
        stock_prices: The query to update up to 100 stocks of alphabetically
        logged_in_user_id: The logged-in user_id
        sample_portfolio: Places sample portfolio into database portfolio
    """
    response = client.post(f"""/portfolio/{logged_in_user_id}/{sample_portfolio}""")
    assert response.status_code == HTTP_SUCCESS_CODE

    for i in range(1, 9):
        response = client.post(f"""/portfolio/{logged_in_user_id}/{sample_portfolio}/{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == logged_in_user_id).all()) == 10


def test_add_multiple_stocks_to_different_portfolios(client: FlaskClient, client_accounts: list[dict], symbols: None,
                                                     stock_prices: None, logged_in_user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN multiple stock_ids
    WHEN a user is logged in and wants to add a stock to a particular portfolio (and already has multiple portfolios)
    THEN check that the new stocks corresponds to the sample portfolio
    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients
        symbols: The query to create stock symbol rows
        stock_prices: The query to update up to 100 stocks of alphabetically
        logged_in_user_id: The logged-in user_id
        sample_portfolio: Places sample portfolio into database portfolio
    """
    response = client.post(f"""/portfolio/{logged_in_user_id}/{sample_portfolio}""")
    assert response.status_code == HTTP_SUCCESS_CODE

    response = client.post(f"""/portfolio/{logged_in_user_id}/sample_portfolio_2""")
    assert response.status_code == HTTP_SUCCESS_CODE

    for i in range(1, 9):
        response = client.post(f"""/portfolio/{logged_in_user_id}/{sample_portfolio}/{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == logged_in_user_id,
                                                  Portfolio.portfolio_name == sample_portfolio).all()) == 10


def test_add_invalid_stock_to_portfolio(client: FlaskClient, client_accounts: list[dict], symbols: None,
                                        stock_prices: None, logged_in_user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN an invalid stock_id
    WHEN a user is logged in and wants to add a stock to a particular portfolio
    THEN check that the new stock HAS NOT been added

    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients
        symbols: The query to create stock symbol rows
        stock_prices: The query to update up to 100 stocks of alphabetically
        logged_in_user_id: The logged-in user_id
        sample_portfolio: Places sample portfolio into database portfolio
    """
    response = client.post(f"""/portfolio/{logged_in_user_id}/{sample_portfolio}/-{faker_data.random_number()}""")
    assert response.status_code != HTTP_SUCCESS_CODE

    # Remember that when a portfolio is created, no stocks are added (which still means there's the original row)
    # so we must count it
    assert len(db.session.query(Portfolio.stock_id)
               .filter(Portfolio.user_id == logged_in_user_id).all()) == 1
