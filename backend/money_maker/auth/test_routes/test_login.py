import pytest
from conftest import (HTTP_SUCCESS_CODE, NUMBER_OF_USERS, PASSWORD_LENGTH,
                      REPEAT_TESTS)
from flask.testing import FlaskClient
from money_maker.extensions import faker_data


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_login(flask_application: FlaskClient, user_account: dict) -> None:
    """
    GIVEN a registered user
    WHEN a User logins
    THEN check that the backend responds with a 200 response code

    Args:
        flask_application: The flask application
        user_account: The single registered user.
    """
    response = flask_application.post("/auth/login", json=user_account)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == "login successful"


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_multiple_logins(flask_application: FlaskClient, user_accounts: list[dict]) -> None:
    """
    GIVEN a list of registered users
    WHEN each user attempts to log in
    THEN check that the application responds to each user with a 200 response code.

    Args:
        flask_application (FlaskClient): The flask application
        user_accounts (list[dict]): A list of registered user
    """
    for index in range(NUMBER_OF_USERS):
        response = flask_application.post("/auth/login", json=user_accounts[index])
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == "login successful"


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_email_login(flask_application: FlaskClient, user_account: dict) -> None:
    """
    GIVEN a newly generated email from faker
    WHEN a registered user with their new email attempts to log in (even with a correct passsword)
    THEN check the application does not log them into the application.

    Args:
        flask_application (FlaskClient): The flask application
        user_account (dict): The single registered user.
    """
    altered_account = {
        "body": faker_data.ascii_email(),
        "password": user_account["password"]
    }
    response = flask_application.post("/auth/login", json=altered_account)
    assert response.status_code != HTTP_SUCCESS_CODE
    assert response.get_json()["error"] == "Missing credentials or wrong login"


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_multiple_email_logins(flask_application: FlaskClient, user_accounts: list[dict]) -> None:
    """
    GIVEN several newly generated emails from faker
    WHEN a user with their new email attempts to log in
    THEN check the application does not log them into the application.

    Args:
        flask_application (FlaskClient): The flask application
        user_accounts (dict): A list of registered user
    """
    for user in user_accounts:
        altered_account = {
            "body": faker_data.ascii_email(),
            "password": user["password"]
        }
        response = flask_application.post("/auth/login", json=altered_account)
        assert response.status_code != HTTP_SUCCESS_CODE
        assert response.get_json()["error"] == "Missing credentials or wrong login"


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_password_login(flask_application: FlaskClient, user_account: dict) -> None:
    """
    GIVEN a newly generated valid password from faker
    WHEN a registered user with their new password attempts to log in (even with a correct email)
    THEN check the application does not log them into the application.

    Args:
        flask_application (FlaskClient): The flask application
        user_account (dict): The single registered user.
    """
    altered_account = {
        "body": user_account["email"],
        "password": faker_data.password(length=PASSWORD_LENGTH, special_chars=False)
    }
    response = flask_application.post("/auth/login", json=altered_account)
    assert response.status_code != HTTP_SUCCESS_CODE
    assert response.get_json()["error"] == "Missing credentials or wrong login"


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_multiple_password_logins(flask_application: FlaskClient, user_accounts: list[dict]) -> None:
    """
    GIVEN several newly generated emails from faker
    WHEN a user with their new password attempts to log in
    THEN check the application does not log them into the application.

    Args:
        flask_application (FlaskClient): The flask application
        user_accounts (list[dict]): The single registered user.
    """
    for user in user_accounts:
        altered_account = {
            "body": user["email"],
            "password": faker_data.password(length=PASSWORD_LENGTH, special_chars=False)
        }
        response = flask_application.post("/auth/login", json=altered_account)
        assert response.status_code != HTTP_SUCCESS_CODE
        assert response.get_json()["error"] == "Missing credentials or wrong login"


def test_no_json_login(flask_application: FlaskClient) -> None:
    """
    GIVEN a request that provides no json
    WHEN a user attempts to log in
    THEN check the application rejects this login

    Args:
        flask_application (FlaskClient): The flask application
    """
    response = flask_application.post("/auth/login")
    assert response.status_code != HTTP_SUCCESS_CODE
    assert response.get_json() is None


def test_empty_login(flask_application: FlaskClient) -> None:
    """
    GIVEN a request that provides empty user details
    WHEN a user attempts to log in
    THEN check the application rejects this login

    Args:
        flask_application (FlaskClient): The flask application
    """
    user_details = {
        "email": "",
        "password": ""
    }
    response = flask_application.post("/auth/login", json=user_details)
    assert response.status_code != HTTP_SUCCESS_CODE
    assert response.get_json()["error"] == "Missing credentials or wrong login"
