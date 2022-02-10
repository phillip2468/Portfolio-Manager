import flask
import pytest
from conftest import HTTP_SUCCESS_CODE, NUMBER_OF_USERS, REPEAT_TESTS


@pytest.mark.repeat(REPEAT_TESTS)
def test_which_user(client, client_accounts) -> None:
    """
    GIVEN a registered user
    WHEN attempts to find out which user they are
    THEN check that the backend responds with a 200 response code

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
    GIVEN a registered user
    WHEN attempts to find out which user they are
    THEN check that the backend does not responds with a 200 response code

    :param client: The flask app
    :type client: flask.testing.FlaskClient
    :param client_accounts: The dictionary of users
    :type client_accounts: dict
    """
    client.cookie_jar.clear()
    response: flask.Response = client.get("/auth/which_user")
    assert response.status_code != HTTP_SUCCESS_CODE


