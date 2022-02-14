from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, UPDATE_STOCK_TO_PORTFOLIO, ADD_STOCK_TO_PORTFOLIO
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio, portfolio_schema


def test_update_portfolio_stock_details(flask_application: FlaskClient, user_account_logged_in: dict,
                                        user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN a stock id
    WHEN a user is logged in and wants to update the stock price and units of a stock
    THEN check that the new details have been updated

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
        sample_portfolio: The name of the sample portfolio
    """

    response = flask_application.post(f"""/portfolio/{user_id}/{sample_portfolio}/1""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == ADD_STOCK_TO_PORTFOLIO

    updated_stock_details = {
        "units_price": 100,
        "units_purchased": 1000
    }
    response = flask_application.patch(f"""/portfolio/{user_id}/{sample_portfolio}/1""", json=updated_stock_details)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_STOCK_TO_PORTFOLIO

    portfolio_stock: Portfolio = db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                                    Portfolio.portfolio_name == sample_portfolio,
                                                                    Portfolio.stock_id == 1).one_or_none()
    assert portfolio_stock is not None
    assert portfolio_stock.units_purchased == 1000
    assert portfolio_stock.units_price == 100


def test_update_portfolio_one_stock_details(flask_application: FlaskClient, user_account_logged_in: dict,
                                            user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN a stock id and a portfolio
    WHEN a user is logged in and wants to update the stock price and units of one stock
    THEN check that the new details have been updated for that particular stock, and that
    no other rows are affected.

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
        sample_portfolio: The name of the sample portfolio
    """

    for i in range(1, 10):
        response = flask_application.post(f"""/portfolio/{user_id}/{sample_portfolio}/{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == ADD_STOCK_TO_PORTFOLIO

    updated_stock_details = {
        "units_price": 100,
        "units_purchased": 1000
    }
    response = flask_application.patch(f"""/portfolio/{user_id}/{sample_portfolio}/1""", json=updated_stock_details)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_STOCK_TO_PORTFOLIO

    portfolio_stock: Portfolio = db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                                    Portfolio.portfolio_name == sample_portfolio,
                                                                    Portfolio.stock_id == 1).one_or_none()
    assert portfolio_stock is not None
    assert portfolio_stock.units_purchased == 1000
    assert portfolio_stock.units_price == 100

    for i in range(2, 10):
        pf_stock = db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                      Portfolio.portfolio_name == sample_portfolio,
                                                      Portfolio.stock_id == i).one_or_none()
        pf_stock_object = portfolio_schema.dump(pf_stock)
        assert pf_stock_object["units_price"] == 0
        assert pf_stock_object["units_purchased"] == 0
