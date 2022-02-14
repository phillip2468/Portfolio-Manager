from flask.testing import FlaskClient

from conftest import (CREATE_PORTFOLIO_MSG, HTTP_SUCCESS_CODE, UPDATE_PORTFOLIO_MSG, ADD_STOCK_TO_PORTFOLIO,
                      LOGIN_SUCCESS_MSG)
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio


def test_update_portfolio_name(flask_application: FlaskClient, user_account_logged_in: dict, user_id: int) -> None:
    """
    GIVEN a user that has a portfolio
    WHEN a user wants to update the name of this portfolio
    THEN check that the portfolio's name has been changed to the new entry

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
    """

    response = flask_application.post(f"""/portfolio/{user_id}/sample_portfolio""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == CREATE_PORTFOLIO_MSG

    new_pf_name = {
        "portfolio_name": "new_pf_name"
    }
    response = flask_application.patch(f"""/portfolio/{user_id}/sample_portfolio""", json=new_pf_name)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_PORTFOLIO_MSG

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                  Portfolio.portfolio_name == "sample_portfolio").all()) == 0

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                  Portfolio.portfolio_name == "new_pf_name").all()) == 1
    db.session.query(Portfolio).delete(synchronize_session="fetch")
    db.session.commit()


def test_update_one_portfolio_name(flask_application: FlaskClient, user_account_logged_in: dict, user_id: int) -> None:
    """
    GIVEN a user that has multiple portfolios
    WHEN a user wants to update the name of one of their portolfios
    THEN check that ONLY one of these portfolios is changed

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
    """

    for i in range(1, 5):
        response = flask_application.post(f"""/portfolio/{user_id}/sample_portfolio_{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == CREATE_PORTFOLIO_MSG

    new_pf_name = {
        "portfolio_name": "new_pf_name"
    }
    response = flask_application.patch(f"""/portfolio/{user_id}/sample_portfolio_1""", json=new_pf_name)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_PORTFOLIO_MSG

    for i in range(2, 5):
        assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                      Portfolio.portfolio_name == f"""sample_portfolio_{i}""")
                   .all()) == 1

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                  Portfolio.portfolio_name == "new_pf_name").all()) == 1
    db.session.query(Portfolio).delete(synchronize_session="fetch")
    db.session.commit()


def test_update_portfolio_name_with_stocks(flask_application: FlaskClient, user_account_logged_in: dict,
                                           user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN a user that has a portfolio
    WHEN a user wants to update the name of this portfolio
    THEN check that the portfolio's name has been changed to the new entry along with the other rows containg the stocks

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
    """

    for i in range(1, 10):
        response = flask_application.post(f"""/portfolio/{user_id}/{sample_portfolio}/{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == ADD_STOCK_TO_PORTFOLIO

    new_pf_name = {
        "portfolio_name": "new_pf_name"
    }
    response = flask_application.patch(f"""/portfolio/{user_id}/{sample_portfolio}""", json=new_pf_name)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_PORTFOLIO_MSG

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                  Portfolio.portfolio_name == sample_portfolio).all()) == 0

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                  Portfolio.portfolio_name == "new_pf_name").all()) == 10
    db.session.query(Portfolio).delete(synchronize_session="fetch")
    db.session.commit()


def test_update_one_portfolio_name_with_stocks(flask_application: FlaskClient, user_account_logged_in: dict,
                                               user_id: int) -> None:
    """
    GIVEN a user that has 5 portfolios
    WHEN a user wants to update the name of a portfolio
    THEN check that the portfolio's name has been changed to the new entry along and that other portfolio's name
    has not been changed

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
    """

    for i in range(1, 5):
        response = flask_application.post(f"""/portfolio/{user_id}/sample_portfolio_{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == CREATE_PORTFOLIO_MSG
        for j in range(1, 10):
            response = flask_application.post(f"""/portfolio/{user_id}/sample_portfolio_{i}/{j}""")
            assert response.status_code == HTTP_SUCCESS_CODE
            assert response.get_json()["msg"] == ADD_STOCK_TO_PORTFOLIO

    new_pf_name = {
        "portfolio_name": "new_pf_name"
    }
    response = flask_application.patch(f"""/portfolio/{user_id}/sample_portfolio_1""", json=new_pf_name)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_PORTFOLIO_MSG

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                  Portfolio.portfolio_name == "sample_portfolio_1").all()) == 0

    for i in range(2, 5):
        assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                      Portfolio.portfolio_name == f"""sample_portfolio_{i}""").all()) \
               == 10

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                  Portfolio.portfolio_name == "new_pf_name").all()) == 10
    db.session.query(Portfolio).delete(synchronize_session="fetch")
    db.session.commit()


def test_invalid_update_portfolio_name(flask_application: FlaskClient, user_accounts: list[dict]) -> None:
    """
    GIVEN a portfolio
    WHEN another user attempts to update a portfolio that is not theirs
    THEN check that the new portfolio name IS NOT applied

    Args:
        flask_application: The flask application
        user_accounts: The list of dictionaries of registered users
    """
    response = flask_application.post("/auth/login", json=user_accounts[0])
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == LOGIN_SUCCESS_MSG

    response = flask_application.get("/auth/which_user")
    assert response.status_code == HTTP_SUCCESS_CODE
    user_id = response.get_json()["user_id"]

    response = flask_application.post(f"""/portfolio/{user_id}/sample_portfolio""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == CREATE_PORTFOLIO_MSG

    response = flask_application.post("/auth/login", json=user_accounts[1])
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == LOGIN_SUCCESS_MSG

    new_pf_name = {
        "portfolio_name": "new_pf_name"
    }
    response = flask_application.patch(f"""/portfolio/{user_id}/sample_portfolio""", json=new_pf_name)
    assert response.status_code != HTTP_SUCCESS_CODE

    # Remember that the empty portfolio still exists in the database
    assert len(db.session.query(Portfolio.user_id == user_id).all()) == 1

    db.session.query(Portfolio).filter(Portfolio.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()
