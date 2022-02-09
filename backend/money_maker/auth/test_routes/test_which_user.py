import flask
import pytest
from conftest import HTTP_SUCCESS_CODE, NUMBER_OF_USERS, REPEAT_TESTS


@pytest.mark.repeat(REPEAT_TESTS)
def test_which_user(client, client_accounts) -> None:
    """
    Tests that the system can find the user using cookies from the
    request. Returns a dictionary containing a user_id.
    Useful for identifying other features that are related to a user
    in the database.

    :param client: The flask app
    :type client: flask.testing.FlaskClient
    :param client_accounts: The dictionary of users
    :type client_accounts: dict
    """
    for i in range(NUMBER_OF_USERS):
        response: flask.Response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code == HTTP_SUCCESS_CODE

        response: flask.Response = client.get("/auth/which_user")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["user_id"] == i + 1


@pytest.mark.repeat(REPEAT_TESTS)
def test_which_user_invalid(client, client_accounts) -> None:
    """
    Tests unauthorized route status by clearing cookies of client
    response.

    :param client: The flask app
    :type client: flask.testing.FlaskClient
    :param client_accounts: The dictionary of users
    :type client_accounts: dict
    """
    client.cookie_jar.clear()
    response: flask.Response = client.get("/auth/which_user")
    assert response.status_code != HTTP_SUCCESS_CODE


