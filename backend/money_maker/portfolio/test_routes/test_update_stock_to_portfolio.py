from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, UPDATE_STOCK_TO_PORTFOLIO, ADD_STOCK_TO_PORTFOLIO, CREATE_PORTFOLIO_MSG
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


def test_one_update_portfolio_one_stock_details(flask_application: FlaskClient, user_account_logged_in: dict,
                                                user_id: int) -> None:
    """
    GIVEN a stock id and a portfolio and the user has multiple portfolios
    WHEN a user is logged in and wants to update the stock price and units of one stock
    THEN check that the new details have been updated for that particular stock, and that
    no other rows are affected.

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user

    """
    for pf in range(1, 5):
        response = flask_application.post(f"""/portfolio/{user_id}/sample_pf_{pf}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == CREATE_PORTFOLIO_MSG
        for stock_id in range(1, 10):
            response = flask_application.post(f"""/portfolio/{user_id}/sample_pf_{pf}/{stock_id}""")
            assert response.status_code == HTTP_SUCCESS_CODE
            assert response.get_json()["msg"] == ADD_STOCK_TO_PORTFOLIO

    updated_stock_details = {
        "units_price": 1000,
        "units_purchased": 1000
    }

    response = flask_application.patch(f"""/portfolio/{user_id}/sample_pf_1/1""", json=updated_stock_details)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_STOCK_TO_PORTFOLIO

    changed_stock = db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                       Portfolio.portfolio_name == "sample_pf_1",
                                                       Portfolio.stock_id == 1).one_or_none()
    as_object_stock = portfolio_schema.dump(changed_stock)
    assert as_object_stock["units_price"] == 1000
    assert as_object_stock["units_purchased"] == 1000

    for stock_id in range(2, 10):
        stock = db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                   Portfolio.portfolio_name == "sample_pf_1",
                                                   Portfolio.stock_id == stock_id).one_or_none()
        assert stock is not None
        pf_stock_object = portfolio_schema.dump(stock)
        assert pf_stock_object["units_price"] == 0
        assert pf_stock_object["units_purchased"] == 0

    for pf in range(2, 5):
        for stock_id in range(1, 10):
            stock = db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                       Portfolio.portfolio_name == f"""sample_pf_{pf}""",
                                                       Portfolio.stock_id == stock_id).one_or_none()
            assert stock is not None
            pf_stock_object = portfolio_schema.dump(stock)
            assert pf_stock_object["units_price"] == 0
            assert pf_stock_object["units_purchased"] == 0

    db.session.query(Portfolio).delete(synchronize_session="fetch")
    db.session.commit()


def test_invalid_update_stock_to_other_users_portfolio(flask_application: FlaskClient, user_accounts: list[dict]) -> None:
    """
    GIVEN a valid stock id and portfolio
    WHEN a user is logged in and attempts to add a portfolio from another user
    THEN check that the new stock details has not been added/ updated


    Args:
        flask_application: The flask application
        user_accounts: List of dictionaries of other accounts
    """

    response = flask_application.post("/auth/login", json=user_accounts[0])
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == "login successful"

    response = flask_application.get("/auth/which_user")
    assert response.status_code == HTTP_SUCCESS_CODE
    user_id = int(response.get_json()["user_id"])

    response = flask_application.post(f"""/portfolio/{user_id}/user_1_pf""")
    assert response.status_code == HTTP_SUCCESS_CODE

    response = flask_application.post(f"""/portfolio/{user_id}/user_1_pf/1""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == ADD_STOCK_TO_PORTFOLIO

    updated_stock_details = {
        "units_price": 1000,
        "units_purchased": 1000
    }
    response = flask_application.patch(f"""/portfolio/{user_id}/user_1_pf/1""", json=updated_stock_details)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_STOCK_TO_PORTFOLIO

    response = flask_application.post("/auth/login", json=user_accounts[1])
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == "login successful"

    response = flask_application.patch(f"""/portfolio/{user_id}/user_1_pf/1""", json=updated_stock_details)
    assert response.status_code != HTTP_SUCCESS_CODE

    db.session.query(Portfolio).filter(Portfolio.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()
