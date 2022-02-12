import pytest
from flask.testing import FlaskClient

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


@pytest.fixture(scope="session")



@pytest.fixture(scope="function")
def client():
    """
    Creates the sample flask client required for pytests.

    Yields:
        FlaskClient: The example flask application
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
def client_accounts(client: FlaskClient) -> list[dict]:
    """
    Creates a list of sample users in the database, using random values.
    Returns a dictionary containing an email and unhashed password.

    Args:
        client: The flask application

    Yields:
        list[dict[str, str]]: The list of users
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
def symbols(client: FlaskClient) -> None:
    """
    A query which creates all the rows that contain the symbols in the database.

    Args:
        client: The flask application
    """
    response = client.get("/ticker/refresh-asx-symbols")
    assert response.status_code == HTTP_SUCCESS_CODE

    response = client.get("/ticker/refresh-us-symbols")
    assert response.status_code == HTTP_SUCCESS_CODE


@pytest.fixture
def stock_prices(client: FlaskClient, symbols: None) -> None:
    """
    A fixture which updates up to 100 stocks of alphabetically
    ordred stocks.

    Args:
        client: The flask application
        symbols: The query to create stock symbol rows

    Returns:

    """
    response = client.get("/task")
    assert response.status_code == HTTP_SUCCESS_CODE


@pytest.fixture
def logged_in_user_id(client: FlaskClient, client_accounts: list[dict]) -> int:
    """
    Provides the user_id pertaining to the registered user.

    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients

    Yields:
        The user id of the logged-in user.

    """
    response = client.post("/auth/login", json=client_accounts[0])
    assert response.status_code == HTTP_SUCCESS_CODE

    response = client.get("/auth/which_user")
    yield response.get_json()["user_id"]


@pytest.fixture
def sample_portfolio(client: FlaskClient, client_accounts: list[dict], symbols: None,
                     stock_prices: None, logged_in_user_id: int) -> str:
    """
    A fixture which creates a sample portfolio in the database. Note that this does not
    contain any stocks by itself.

    Args:
        client: The flask application
        client_accounts: The list of dictionaries of clients
        symbols: The query to create stock symbol rows
        stock_prices: The query to update up to 100 stocks of alphabetically
        logged_in_user_id: The logged-in user_id

    Returns:
        The portfolio name as a string.

    """
    portfolio_name = f"""{faker_data.first_name()}_portfolio"""
    response = client.post(f"""/portfolio/{logged_in_user_id}/{portfolio_name}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    yield portfolio_name
