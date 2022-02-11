import pytest
from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, NUMBER_OF_USERS, REPEAT_TESTS


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_login(client: FlaskClient, client_accounts: list[dict]) -> None:
    """
    GIVEN a registered user
    WHEN a User logins
    THEN check that the backend responds with a 200 response code
    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients
    """

    for i in range(NUMBER_OF_USERS):
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code == HTTP_SUCCESS_CODE


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_email_login(client: FlaskClient, client_accounts: list[dict]) -> None:
    """
    GIVEN a registered user with an invalid email
    WHEN a User logins
    THEN check that the backend does not respond with a 200 response code

    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients

    """
    for i in range(NUMBER_OF_USERS):
        client_accounts[i]["email"] = client_accounts[i]["email"] + 'e'
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code != HTTP_SUCCESS_CODE


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_email_pw(client: FlaskClient, client_accounts: list[dict]) -> None:
    """
    GIVEN a registered user with an invalid password
    WHEN a User logins
    THEN check that the backend does not respond with a 200 response code

    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients

    """
    for i in range(NUMBER_OF_USERS):
        client_accounts[i]["password"] = client_accounts[i]["password"] + 'e'
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code != HTTP_SUCCESS_CODE

