import pytest
from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, NUMBER_OF_USERS, REPEAT_TESTS


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_logout(client: FlaskClient, client_accounts: list[dict]) -> None:
    """
    GIVEN a user
    WHEN a User logout
    THEN check that the backend provides a 200 response

    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients

    """
    for i in range(NUMBER_OF_USERS):
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code == HTTP_SUCCESS_CODE

        response = client.post("/auth/logout")
        assert response.status_code == HTTP_SUCCESS_CODE
