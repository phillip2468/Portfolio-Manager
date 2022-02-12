import pytest
from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, REPEAT_TESTS


@pytest.mark.repeat(REPEAT_TESTS)
def test_which_user(flask_application: FlaskClient, user_account_logged_in: dict) -> None:
    """
    GIVEN a registered user
    WHEN attempts to find out which user they are
    THEN check that the backend responds with a 200 response code

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged into the flask application.
    """

    response = flask_application.get("/auth/which_user")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["user_id"] == 1


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_which_user_no_cookies(flask_application: FlaskClient, user_account_logged_in: dict) -> None:
    """
    GIVEN a registered user who has cleared their cookies
    WHEN attempts to find out which user they are
    THEN check that the backend does not respond with a 200 response code

    Args:
        flask_application: The flask application
        user_account_logged_in: The single registered user logged into the flask application.
    """
    flask_application.cookie_jar.clear()
    response = flask_application.get("/auth/which_user")
    assert response.status_code != HTTP_SUCCESS_CODE
