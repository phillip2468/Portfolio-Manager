import pytest
from conftest import HTTP_SUCCESS_CODE, NUMBER_OF_USERS, REPEAT_TESTS


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_logout(client, client_accounts) -> None:
    """
    GIVEN a user
    WHEN a User logout
    THEN check that the backend provides a 200 response

    :param client: the flask app
    :param client_accounts: a dictionary containing the user details
    """
    for i in range(NUMBER_OF_USERS):
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code == HTTP_SUCCESS_CODE

        response = client.post("/auth/logout")
        assert response.status_code == HTTP_SUCCESS_CODE
