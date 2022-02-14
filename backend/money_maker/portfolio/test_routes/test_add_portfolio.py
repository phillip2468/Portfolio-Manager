import pytest
from conftest import HTTP_SUCCESS_CODE, REPEAT_TESTS
from flask.testing import FlaskClient
from money_maker.extensions import db
from money_maker.models.portfolio import Portfolio
from money_maker.models.user import User


@pytest.mark.repeat(REPEAT_TESTS)
def test_add_portfolio(flask_application: FlaskClient, user_account, user_account_logged_in: dict, user_id: int) -> None:
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


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_user_add_portfolio(flask_application: FlaskClient, user_account: dict, user_account_logged_in: dict,
                                    user_id: int) -> None:
    """
    GIVEN a portfolio name
    WHEN ANOTHER USER attempts to add a portfolio to the another user's account
    THEN check that the request is rejected and an error code is presented.

    Args:
        flask_application : The flask application
        user_account : The single registered user logged in.
        user_account_logged_in : The id of the user

    """
    other_user = {
        "email": "anotheruser1@email.com",
        "password": "Password12345"
    }
    response = flask_application.post("/auth/register", json=other_user)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == "register successful"

    response = flask_application.post(f"""/portfolio/{user_id}/example""")
    assert response.status_code != HTTP_SUCCESS_CODE
    assert response.get_json()["error"] == "not a valid user"

    db.session.query(User).filter(User.email == other_user["email"]).delete(synchronize_session="fetch")
    db.session.commit()

    assert len(db.session.query(User).all()) == 1

