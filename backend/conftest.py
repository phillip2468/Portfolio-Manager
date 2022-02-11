import pytest
import urllib3
from money_maker.app import create_test_app
from money_maker.extensions import db, faker_data
from money_maker.models.user import User

REPEAT_TESTS = 1
HTTP_SUCCESS_CODE = 200
PASSWORD_LENGTH = 10
NUMBER_OF_USERS = 3

MIN_LENGTH_EMAIL = 8
MAX_LENGTH_EMAIL = 100

# 'Passwords must contain a lowercase and uppercase letter, a digit and be greater than 8 characters.'
# 'Email addresses should be longer than 10 characters, contain an @ symbol and should contain a domain.'

# Remember that you can't have [False, False] for casing as there would be no letters!
LETTER_CASINGS = [[True, True], [True, False], [False, True]]


@pytest.fixture(scope="function")
def client():
    """
    Creates the sample flask client required for pytests.
    :return: The flask client
    :rtype: FlaskClient
    """
    test_app = create_test_app()
    with test_app.test_client() as flask_client:
        with test_app.app_context():
            db.create_all()
            yield flask_client
            db.session.remove()
            db.drop_all()
            flask_client.cookie_jar.clear()
            flask_client.cookie_jar.clear_session_cookies()


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


@pytest.fixture
def symbols(client):
    response = client.get("/ticker/refresh-asx-symbols")
    assert response.status_code == HTTP_SUCCESS_CODE

    response = client.get("/ticker/refresh-us-symbols")
    assert response.status_code == HTTP_SUCCESS_CODE


@pytest.fixture
def stock_prices(client, symbols):
    """
    A fixture which updates up to 100 stocks of alphabetically
    ordred stocks.

    :param client: The flask client
    :type client: FlaskClient
    :param symbols: The fixture which inserts the stock symbols
    :type symbols: Any
    """
    response = client.get("/task")
    assert response.status_code == HTTP_SUCCESS_CODE


@pytest.fixture
def logged_in_user_id(client, client_accounts):
    response = client.post("/auth/login", json=client_accounts[0])
    assert response.status_code == HTTP_SUCCESS_CODE

    response = client.get("/auth/which_user")
    yield response.get_json()["user_id"]

