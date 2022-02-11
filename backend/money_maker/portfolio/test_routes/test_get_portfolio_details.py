from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio


def test_get_all_portfolios(client: FlaskClient, client_accounts: list[dict], symbols: None,
                            stock_prices: None, logged_in_user_id: int) -> None:
    """
    GIVEN a user id
    WHEN a user is logged in
    THEN check that all portfolios are returned for the user

    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients
        symbols: The query to create stock symbol rows
        stock_prices: The query to update up to 100 stocks of alphabetically
        logged_in_user_id: The logged-in user_id
    """

    for i in range(1, 5):
        response = client.post(f"""/portfolio/{logged_in_user_id}/sample_portfolio{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio)
               .filter(Portfolio.user_id == logged_in_user_id).all()) > 1

    response = client.get(f"""/portfolio/{logged_in_user_id}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(response.get_json()) > 1


def test_get_all_stocks_from_portfolio(client: FlaskClient, client_accounts: list[dict], symbols: None,
                                       stock_prices: None, logged_in_user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN a user id
    WHEN a user is logged in
    THEN check that all stocks from a portfolios are returned for the user

    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients
        symbols: The query to create stock symbol rows
        stock_prices: The query to update up to 100 stocks of alphabetically
        logged_in_user_id: The logged-in user_id
        sample_portfolio: Places sample portfolio into database portfolio

    """

    assert len(db.session.query(Portfolio)
               .filter(Portfolio.user_id == logged_in_user_id).all()) == 1

    for i in range(1, 10):
        response = client.post(f"""/portfolio/{logged_in_user_id}/{sample_portfolio}/{i}""")
        assert response.status_code == 200

    response = client.get(f"""/portfolio/{logged_in_user_id}/{sample_portfolio}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(response.get_json()) == 9
