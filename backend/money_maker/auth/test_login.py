import pytest

from money_maker.app import create_test_app
from money_maker.extensions import db, faker_data
from money_maker.models.user import User

REPEAT_TESTS = 1


@pytest.fixture(scope="function")
def client():
    test_app = create_test_app()
    with test_app.test_client() as flask_client:
        with test_app.app_context():
            db.create_all()
        yield flask_client
        db.drop_all()


@pytest.fixture
def client_account(client):
    """
    Creates a sample user in the database, using random values.
    Returns a dictionary containing an email and unhashed password.

    :param client: the flask app
    :return: dict
    """
    email = faker_data.ascii_email()
    password = faker_data.password(length=10, special_chars=False)
    body = {
        "email": email,
        "password": password
    }
    response = client.post("/auth/register", json=body)
    assert response.status_code == 200
    assert len(db.session.query(User).all()) == 1
    yield body


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_login(client, client_account):
    """
    Register an account with valid details by providing an email
    and password, and check in the backend that these values have been
    inserted.
    """

    response = client.post("/auth/login", json=client_account)
    assert response.status_code == 200
