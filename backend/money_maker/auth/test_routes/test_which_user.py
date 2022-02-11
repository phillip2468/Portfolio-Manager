import pytest
from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, NUMBER_OF_USERS, REPEAT_TESTS


@pytest.mark.repeat(REPEAT_TESTS)
def test_which_user(client: FlaskClient, client_accounts: list[dict]) -> None:
    """
    GIVEN a registered user
    WHEN attempts to find out which user they are
    THEN check that the backend responds with a 200 response code

    Args:
        client: The flask app
        client_accounts: List of dict
    """

    for i in range(NUMBER_OF_USERS):
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code == HTTP_SUCCESS_CODE

        response = client.get("/auth/which_user")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["user_id"] == i + 1


@pytest.mark.repeat(REPEAT_TESTS)
def test_which_user_invalid(client: FlaskClient, client_accounts: list[dict]) -> None:
    """
    GIVEN a non-registered user who has cleared their cookies
    WHEN attempts to find out which user they are
    THEN check that the backend does not respond with a 200 response code

    Args:
        client: The flask app
        client_accounts: List of dict

    """
    client.cookie_jar.clear()
    response = client.get("/auth/which_user")
    assert response.status_code != HTTP_SUCCESS_CODE


