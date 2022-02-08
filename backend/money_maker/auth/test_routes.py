import random

import pytest

from money_maker.app import create_test_app
from money_maker.extensions import db, faker_data
from money_maker.models.user import User

REPEAT_TESTS = 1

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
        body = {
            "email": faker_data.name(),
            "password": faker_data.password(length=10, special_chars=False)
        }
        client.post("/auth/register", json=body)


@pytest.mark.repeat(REPEAT_TESTS)
def test_invalid_register_short_pw(create_app):
    """
    Tests that an invalid password cannot be entered. In this case, passwords
    shorter than 8 characters cannot be entered.

    :param create_app: The flask app fixture
    :type create_app: flask.app.Flask
    """
    with create_app.test_client() as client, pytest.raises(ValueError):
        body = {
            "email": faker_data.ascii_email(),
            "password": faker_data.password(length=random.randint(1, 7), special_chars=False,
                                            digits=False, upper_case=False, lower_case=True)
        }
        client.post("/auth/register", json=body)
