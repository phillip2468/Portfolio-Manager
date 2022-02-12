import pytest
from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, REPEAT_TESTS
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio

NUMBER_OF_PFS = 5
NUMBER_OF_STOCKS = 10


@pytest.mark.repeat(REPEAT_TESTS)
def test_add_stock_to_portfolio(flask_application: FlaskClient, user_account_logged_in: dict,
                                user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN a stock id
    WHEN a user is logged in and wants to add a stock to portfolio
    THEN check that the new stock has been added

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
        sample_portfolio: The name of the sample portfolio
    """

    response = flask_application.post(f"""/portfolio/{user_id}/{sample_portfolio}/1""")
    assert response.status_code == HTTP_SUCCESS_CODE

    db.session.query(Portfolio).filter(Portfolio.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()

    assert len(db.session.query(Portfolio).all()) == 0


def test_add_multiple_stocks_to_portfolio(flask_application: FlaskClient, user_account_logged_in: dict,
                                          user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN multiple stock_ids
    WHEN a user is logged in and wants to add a stock to portfolio
    THEN check that the new stock has been added
    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
        sample_portfolio: The name of the sample portfolio
    """

    for i in range(1, 10):
        response = flask_application.post(f"""/portfolio/{user_id}/{sample_portfolio}/{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id).all()) == 10
    db.session.query(Portfolio).filter(Portfolio.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()
    assert len(db.session.query(Portfolio).all()) == 0


def test_add_multiple_stocks_to_different_portfolios(flask_application: FlaskClient, user_account_logged_in: dict,
                                                     user_id: int) -> None:
    """
    GIVEN multiple stock_ids
    WHEN a user is logged in and wants to add a stock to a particular portfolio (and already has multiple portfolios)
    THEN check that the new stocks corresponds to the sample portfolio
    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
    """
    for i in range(NUMBER_OF_PFS):
        response = flask_application.post(f"""/portfolio/{user_id}/sample_portfolio_{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == "Successfully created a new portfolio"

    for pf_index in range(NUMBER_OF_PFS):
        pf_name = f"""sample_portfolio_{pf_index}"""
        for stock_index in range(1, NUMBER_OF_STOCKS):
            response = flask_application.post(f"""/portfolio/{user_id}/{pf_name}/{stock_index}""")
            assert response.status_code == HTTP_SUCCESS_CODE
            assert response.get_json()["msg"] == "Successfully added stock"
        assert len(db.session.query(Portfolio).filter(Portfolio.user_id == user_id,
                                                      Portfolio.portfolio_name == pf_name).all()) == NUMBER_OF_STOCKS

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id ==
                                                  user_id).all()) == NUMBER_OF_STOCKS * NUMBER_OF_PFS
    db.session.query(Portfolio).filter(Portfolio.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()
    assert len(db.session.query(Portfolio).all()) == 0


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_add_stock_to_portfolio(flask_application: FlaskClient, user_account_logged_in: dict,
                                        user_id: int, sample_portfolio: str) -> None:
    """
    GIVEN a stock id of 0
    WHEN a user is logged in and wants to add a stock to portfolio
    THEN check that the new stock has been not been added

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
        sample_portfolio: The name of the sample portfolio
    """

    response = flask_application.post(f"""/portfolio/{user_id}/{sample_portfolio}/0""")
    assert response.status_code != HTTP_SUCCESS_CODE

    # Remember that the original portfolio still has a length of 1!
    assert len(db.session.query(Portfolio).all()) == 1

