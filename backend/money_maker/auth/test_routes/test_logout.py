import pytest
from conftest import (HTTP_SUCCESS_CODE, NUMBER_OF_USERS, PASSWORD_LENGTH,
                      REPEAT_TESTS)


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_logout(client, client_accounts) -> None:
    """
    Login a user into the application with valid account details
    and then log them out.

    :param client: the flask app
    :param client_accounts: a dictionary containing the user details
    """
    for i in range(NUMBER_OF_USERS):
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code == HTTP_SUCCESS_CODE

        response = client.post("/auth/logout")
        assert response.status_code == HTTP_SUCCESS_CODE
