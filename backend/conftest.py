import pytest
from flask.testing import FlaskClient
from money_maker.app import create_test_app
from money_maker.extensions import db, faker_data
from money_maker.models.portfolio import Portfolio
from money_maker.models.user import User

REPEAT_TESTS = 1
HTTP_SUCCESS_CODE = 200
PASSWORD_LENGTH = 10
NUMBER_OF_USERS = 3

MIN_LENGTH_EMAIL = 8
MAX_LENGTH_EMAIL = 100

SAMPLE_PORTFOLIO_NAME = "user_portoflio"

# 'Passwords must contain a lowercase and uppercase letter, a digit and be greater than 8 characters.'
# 'Email addresses should be longer than 10 characters, contain an @ symbol and should contain a domain.'

# Remember that you can't have [False, False] for casing as there would be no letters!
LETTER_CASINGS = [[True, True], [True, False], [False, True]]

LOGIN_SUCCESS_MSG = "login successful"
NEW_PORTFOLIO_SUCCESS_MSG = "Successfully created a new portfolio"


@pytest.fixture(scope="session")
def flask_application() -> FlaskClient:
    """
    Creates the test flask client required for the application.
    Also creates the databases and fills the TickerPrice database
    with the relevant stock symbols.

    Yields:
        The flask test client application.
    """
    flask_app = create_test_app()
    with flask_app.test_client() as test_client:
        with flask_app.app_context():
            db.create_all()
            insert_stock_prices(test_client)

            yield test_client
            db.drop_all()
            test_client.cookie_jar.clear()
            test_client.cookie_jar.clear_session_cookies()


def insert_stock_prices(flask_test_client: FlaskClient) -> None:
    """
    Inserts the stock symbols and information into TickerPrice, necessary for
    querying. Returns nothing.

    Args:
        flask_test_client (FlaskClient):  The test client flask application.
    """
    response = flask_test_client.get("/ticker/refresh-asx-symbols")
    assert response.status_code == HTTP_SUCCESS_CODE
    response = flask_test_client.get("/ticker/refresh-us-symbols")
    assert response.status_code == HTTP_SUCCESS_CODE
    response = flask_test_client.get("/task")
    assert response.status_code == HTTP_SUCCESS_CODE


@pytest.fixture(scope="function")
def user_account(flask_application: FlaskClient) -> dict:
    """
    Generates a sample user for use in the database.
    Once random details has been created return the user
    details. Then after use, the user is deleted and removed from the database.

    Args:
        flask_application (FlaskClient): The test client flask application.

    Yields: A dictionary containing the email and password of the user.

    """
    email = faker_data.ascii_email()
    password = faker_data.password(length=PASSWORD_LENGTH, special_chars=False)
    body = {
        "email": email,
        "password": password
    }
    response = flask_application.post("/auth/register", json=body)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(db.session.query(User).filter(User.email == body["email"]).all()) == 1
    yield body

    response = flask_application.post("/auth/logout")
    assert response.status_code == HTTP_SUCCESS_CODE
    flask_application.cookie_jar.clear()
    db.session.query(User).filter(User.email == body["email"]).delete(synchronize_session="fetch")
    db.session.commit()
    assert len(db.session.query(User).filter(User.email == body["email"]).all()) == 0
    assert len(db.session.query(User).all()) == 0


@pytest.fixture(scope="function")
def user_accounts(flask_application: FlaskClient) -> list[dict]:
    """
    Generates a list of sample users for use in the database.
    Once random details has been created return the list of user
    details. Then after use, each user is deleted and removed from the database.
    Args:
        flask_application (FlaskClient):  The test client flask application.

    Yields:
        The list of user details as a list of dictionaries.
    """
    list_of_users = []
    for i in range(NUMBER_OF_USERS):
        email = faker_data.ascii_email()
        password = faker_data.password(length=PASSWORD_LENGTH, special_chars=False)
        user_details = {
            "email": email,
            "password": password
        }
        response = flask_application.post("/auth/register", json=user_details)
        assert response.status_code == HTTP_SUCCESS_CODE
        assert len(db.session.query(User).filter(User.email == user_details["email"]).all()) == 1
        list_of_users.append(user_details)
        flask_application.cookie_jar.clear()

    assert len(db.session.query(User).all()) == NUMBER_OF_USERS
    yield list_of_users

    for user in list_of_users:
        db.session.query(User).filter(User.email == user["email"]).delete(synchronize_session="fetch")
        db.session.commit()

    assert len(db.session.query(User).all()) == 0
    flask_application.cookie_jar.clear()


@pytest.fixture(scope="function")
def user_account_logged_in(flask_application: FlaskClient, user_account: dict) -> dict:
    """
    Given a registered user, log this user into the flask application. Note that
    the response back will provide cookies and an encoded jwt to verify other requests.

    Args:
        flask_application (FlaskClient):  The test client flask application.
        user_account (dict): A singular registered user account

    Returns:
        The dictionary details of the registered user.
    """
    response = flask_application.post("/auth/login", json=user_account)
    assert response.status_code == HTTP_SUCCESS_CODE
    yield user_account


@pytest.fixture(scope="function")
def user_id(flask_application: FlaskClient, user_account_logged_in: dict) -> int:
    """
    Given a registerd logged-in user, return the user_id of this particular user.

    Args:
        flask_application (FlaskClient):  The test client flask application.
        user_account_logged_in (dict): A singular registered user account that is logged into the application

    Returns:
        The user id as an integer

    """
    response = flask_application.get("/auth/which_user")
    assert response.status_code == HTTP_SUCCESS_CODE
    yield response.get_json()["user_id"]


@pytest.fixture(scope="function")
def sample_portfolio(flask_application: FlaskClient, user_account_logged_in: dict, user_id: int) -> str:
    """
    Creates a sample portfolio for the user and once used, drops it from the database.

    Args:
        flask_application: The test client flask application.
        user_account_logged_in: A singular registered user account that is logged into the application
        user_id: The user id as an intger

    Yields:
        The portfolio name as SAMPLE_PORTFOLIO_NAME + user_account_logged_in["email"]

    """
    pf_name = SAMPLE_PORTFOLIO_NAME + user_account_logged_in["email"]
    response = flask_application.post(f"""/portfolio/{user_id}/{pf_name}""")
    assert response.status_code == HTTP_SUCCESS_CODE

    yield pf_name

    db.session.query(Portfolio).filter(Portfolio.user_id == user_id, Portfolio.portfolio_name == pf_name)\
        .delete(synchronize_session="fetch")
    db.session.commit()

    assert len(db.session.query(Portfolio).filter(Portfolio.user_id).all()) == 0

