import random

import pytest

from money_maker.app import create_test_app
from money_maker.extensions import db, faker_data
from money_maker.models.user import User

HTTP_SUCCESS_CODE = 200

REPEAT_TESTS = 5
valid_password = 'Passwords must contain a lowercase and uppercase letter, a digit and be greater than 8 characters.'
valid_email = 'Email addresses should be longer than 10 characters, contain an @ symbol and should contain a domain.'
min_length_email = 8
max_length_email = 100

# Remember that you can't have [False, False] for casing as there would be no letters!
letter_cases = [[True, True], [True, False], [False, True]]


@pytest.fixture(scope="function")
def client():
    test_app = create_test_app()
    with test_app.test_client() as flask_client:
        with test_app.app_context():
            db.create_all()
        yield flask_client
        db.drop_all()


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_register(client):
    """
    Register an account with valid details by providing an email
    and password, and check in the backend that these values have been
    inserted.

    :param create_app: The flask app fixture
    :type create_app: flask.app.Flask
    """
    body = {
        "email": faker_data.ascii_email(),
        "password": faker_data.password(length=10, special_chars=False)
    }
    response = client.post("/auth/register", json=body)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(db.session.query(User).all()) == 1


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_multiple_register(client):
    """
    Register multiple accounts (2 to 10 times selected randomly) with valid details by providing an email
    and password for each account, and check in the backend that these values have been
    inserted.

    :param create_app: The flask app fixture
    :type create_app: flask.app.Flask
    """
    random_iterations = random.randint(2, 10)
    for i in range(random_iterations):
        body = {
            "email": faker_data.ascii_email(),
            "password": faker_data.password(length=10, special_chars=False)
        }
        response = client.post("/auth/register", json=body)
        assert response.status_code == HTTP_SUCCESS_CODE
        # Note that we must always add 1 to the index as range is a 0 based index
        assert len(db.session.query(User).all()) == i + 1

    assert len(db.session.query(User).all()) == random_iterations


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_register_email(client):
    """
    Tests that an invalid email cannot be entered. In this case, names
    cannot be entered as an email address as they do not contain a
    domain.

    :param client: The flask app fixture
    :type client: flask.app.Flask
    """

    with pytest.raises(ValueError):
        random_num = random.randint(min_length_email, max_length_email)
        body = {
            "email": faker_data.name(),
            "password": faker_data.password(length=random_num,
                                            special_chars=False,
                                            digits=random.choice([True, False]),
                                            upper_case=random.choice([True, False]),
                                            lower_case=True
                                            )
        }
        client.post("/auth/register", json=body)


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_register_short_pw(client):
    """
    Tests that an invalid password cannot be entered. In this case, passwords
    shorter than 8 characters cannot be entered.

    :param client: The flask app fixture
    :type client: flask.app.Flask
    """
    with pytest.raises(ValueError):
        casing = random.choice(letter_cases)
        body = {
            "email": faker_data.ascii_email(),
            "password": faker_data.password(length=random.randint(4, 7),
                                            special_chars=random.choice([True, False]),
                                            digits=random.choice([True, False]),
                                            upper_case=casing[0],
                                            lower_case=casing[1]
                                            )
        }
        client.post("/auth/register", json=body)


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_register_passwords(client):
    """
    Tests that an invalid password cannot be entered. In this case, passwords
    that contain special characters cannot be entered.

    :param client: The flask app fixture
    :type client: flask.app.Flask
    """

    with pytest.raises(ValueError):
        casing = random.choice(letter_cases)
        body = {
            "email": faker_data.ascii_email(),
            "password": faker_data.password(length=random.randint(min_length_email, max_length_email),
                                            special_chars=True,
                                            digits=random.choice([True, False]),
                                            upper_case=casing[0],
                                            lower_case=casing[1])
        }
        client.post("/auth/register", json=body)
