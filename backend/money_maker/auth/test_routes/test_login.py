import pytest
from conftest import HTTP_SUCCESS_CODE, NUMBER_OF_USERS, REPEAT_TESTS


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_login(client, client_accounts) -> None:
    """
    Login a user into the application with valid account details.

    :param client: the flask app
    :param client_accounts: a dictionary containing the user details
    """
    for i in range(NUMBER_OF_USERS):
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code == HTTP_SUCCESS_CODE


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_email_login(client, client_accounts) -> None:
    """
    Login a user into the application invalid account details.
    In this case, the wrong email is entered. To make the test invalid,
    the email is appeneded with an 'e' symbol.

    :param client: the flask app
    :param client_accounts: a dictionary containing the user details
    """
    for i in range(NUMBER_OF_USERS):
        client_accounts[i]["email"] = client_accounts[i]["email"] + 'e'
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code != HTTP_SUCCESS_CODE


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_email_pw(client, client_accounts) -> None:
    """
    Login a user into the application invalid account details.
    In this case, the wrong password is entered.  To make the test invalid,
    the password is appeneded with an 'e' symbol.

    :param client: the flask app
    :param client_accounts: a dictionary containing the user details
    """
    for i in range(NUMBER_OF_USERS):
        client_accounts[i]["password"] = client_accounts[i]["password"] + 'e'
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code != HTTP_SUCCESS_CODE

