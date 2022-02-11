from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio


def test_remove_stock_from_portfolio(client: FlaskClient, client_accounts: list[dict], symbols: None,
                                     stock_prices: None, logged_in_user_id: int) -> None:
    """
    GIVEN a stock id
    WHEN a user is logged in and wants to remove a stock from a portfolio
    THEN check that the new stock has been removed

    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients
        symbols: The query to create stock symbol rows
        stock_prices: The query to update up to 100 stocks of alphabetically
        logged_in_user_id: The logged-in user_id

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
