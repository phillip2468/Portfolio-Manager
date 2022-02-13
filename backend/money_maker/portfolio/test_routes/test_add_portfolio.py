import pytest
from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, REPEAT_TESTS
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio


@pytest.mark.repeat(REPEAT_TESTS)
def test_add_portfolio(flask_application: FlaskClient, user_account_logged_in: dict, user_id: int) -> None:
    """
    GIVEN a portfolio name
    WHEN a user is logged in and wants to create a portfolio
    THEN check that the new portfolio has been created.

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged in.
        user_id: The id of the user
    """

    response = flask_application.post(f"""/portfolio/{user_id}/example""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == "Successfully created a new portfolio"
    assert len(db.session.query(Portfolio).all()) == 1

    db.session.query(Portfolio).filter(Portfolio.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()

    assert len(db.session.query(Portfolio).all()) == 0

