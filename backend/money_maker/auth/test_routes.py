import random

import pytest

from money_maker.app import create_test_app
from money_maker.extensions import db, faker_data
from money_maker.models.user import User

REPEAT_TESTS = 10
valid_password = 'Passwords must contain a lowercase and uppercase letter, a digit and be greater than 8 characters.'
valid_email = 'Email addresses should be longer than 10 characters, contain an @ symbol and should contain a domain.'
min_length_email = 8
max_length_email = 100

@pytest.fixture(scope="function")
def create_app():
    test_app = create_test_app()
    with create_test_app().app_context():
        db.create_all()
        db.session.begin_nested()
        yield test_app
        db.session.rollback()


# noinspection DuplicatedCode
@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_register(create_app):
    """
    Register an account with valid details by providing an email
    and password, and check in the backend that these values have been
    inserted.

    :param create_app: The flask app fixture
    :type create_app: flask.app.Flask
    """
    with create_app.test_client() as client:
        body = {
            "email": faker_data.ascii_email(),
            "password": faker_data.password(length=10, special_chars=False)
        }
        response = client.post("/auth/register", json=body)
        assert response.status_code == 200
        assert len(db.session.query(User).all()) == 1


@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_register_email_with_names(create_app):
    """
    Tests that an invalid email cannot be entered. In this case, names
    cannot be entered as an email address as they do not contain a
    domain.

    :param create_app: The flask app fixture
    :type create_app: flask.app.Flask
    """

    with create_app.test_client() as client, pytest.raises(ValueError):
        random_num = random.randint(min_length_email, max_length_email)
        body = {
            "email": faker_data.name(),
            "password": faker_data.password(length=random_num,
                                            special_chars=False, digits=bool(random.getrandbits(1)),
                                            upper_case=bool(random.getrandbits(1)),
                                            lower_case=bool(random.getrandbits(1)))
        }
        client.post("/auth/register", json=body)


@pytest.mark.repeat(1000)
def test_invalid_register_short_pw(create_app):
    """
    Tests that an invalid password cannot be entered. In this case, passwords
    shorter than 8 characters cannot be entered.

    :param create_app: The flask app fixture
    :type create_app: flask.app.Flask
    """
    random.seed(0)
    with create_app.test_client() as client, pytest.raises(ValueError):
        body = {
            "email": faker_data.ascii_email(),
            "password": faker_data.password(length=random.randint(4, 7),
                                            special_chars=random.choice([True, False]), digits=random.choice([True, False]),
                                            upper_case=random.choice([True, False]), lower_case=random.choice([True, False]))
        }
        client.post("/auth/register", json=body)


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_register_passwords(create_app):
    """
    Tests that an invalid password cannot be entered. In this case, passwords
    that contain special characters cannot be entered.

    :param create_app: The flask app fixture
    :type create_app: flask.app.Flask
    """

    list_of_bools = [faker_data.boolean() for i in range(4)]
    with create_app.test_client() as client, pytest.raises(ValueError):
        body = {
            "email": faker_data.ascii_email(),
            "password": faker_data.password(length=100,
                                            special_chars=True, digits=list_of_bools[1],
                                            upper_case=list_of_bools[2], lower_case=list_of_bools[3])
        }
        client.post("/auth/register", json=body)
