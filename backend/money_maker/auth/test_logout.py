import pytest

from money_maker.app import create_test_app
from money_maker.extensions import db, faker_data
from money_maker.models.user import User

# noinspection DuplicatedCode
REPEAT_TESTS = 2
HTTP_SUCCESS_CODE = 200
PASSWORD_LENGTH = 10
NUMBER_OF_USERS = 3


@pytest.fixture(scope="function")
def client():
    test_app = create_test_app()
    with test_app.test_client() as flask_client:
        with test_app.app_context():
            db.create_all()
        yield flask_client
        db.drop_all()


@pytest.fixture
def client_accounts(client):
    """
    Creates a sample user in the database, using random values.
    Returns a dictionary containing an email and unhashed password.

    :param client: the flask app
    :return: dict
    """
    list_of_clients = []
    for i in range(NUMBER_OF_USERS):
        email = faker_data.ascii_email()
        password = faker_data.password(length=PASSWORD_LENGTH, special_chars=False)
        body = {
            "email": email,
            "password": password
        }
        response = client.post("/auth/register", json=body)
        assert response.status_code == HTTP_SUCCESS_CODE
        list_of_clients.append(body)

    assert len(db.session.query(User).all()) == NUMBER_OF_USERS
    yield list_of_clients


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_logout(client, client_accounts) -> None:
    """
    Login a user into the application with valid account details.

    :param client: the flask app
    :param client_accounts: a dictionary containing the user details
    """
    for i in range(NUMBER_OF_USERS):
        response = client.post("/auth/login", json=client_accounts[i])
        assert response.status_code == HTTP_SUCCESS_CODE

        response = client.post("/auth/logout")
        assert response.status_code == HTTP_SUCCESS_CODE

