import pytest
from conftest import HTTP_SUCCESS_CODE, REPEAT_TESTS
from flask.testing import FlaskClient


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_logout(flask_application: FlaskClient, user_account_logged_in: dict) -> None:
    """
    GIVEN a registered user that is logged in
    WHEN this user attempts to log out
    THEN check that the backend provides a 200 response

    Args:
        flask_application: The flask application
        user_account_logged_in: A registered user logged into the flask application

    """
    response = flask_application.post("/auth/logout")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == "logout successful"


@pytest.mark.repeat(REPEAT_TESTS)
def test_multiple_valid_logouts(flask_application: FlaskClient, user_accounts: dict) -> None:
    """
    GIVEN a list of registered users
    WHEN this user attempts to log out
    THEN check that the backend provides a 200 response
    Args:
        flask_application (FlaskClient):  The flask application
        user_accounts (list[dict]): A list of registered users
    """

    for user in user_accounts:
        response = flask_application.post("/auth/login", json=user)
        assert response.status_code == 200

        response = flask_application.post("/auth/logout")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == "logout successful"
