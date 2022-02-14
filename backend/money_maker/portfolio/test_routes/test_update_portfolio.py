from flask.testing import FlaskClient

from conftest import (CREATE_PORTFOLIO_MSG, HTTP_SUCCESS_CODE, UPDATE_PORTFOLIO_MSG)
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio


def test_update_portfolio_name(flask_application: FlaskClient, user_account_logged_in: dict, user_id: int) -> None:
    """
    GIVEN a user that has a portfolio
    WHEN a user wants to remove this portfolio
    THEN check that the portfolio is removed

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

