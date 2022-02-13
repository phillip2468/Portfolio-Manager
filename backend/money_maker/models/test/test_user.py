import pytest
from conftest import REPEAT_TESTS
from money_maker.extensions import faker_data
from money_maker.models.user import User


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_register_user_details():
    """
    GIVEN valid user_details
    WHEN a new user is created
    THEN check that the email and password are created
    """
    email = faker_data.ascii_email()
    password = faker_data.password(length=10, special_chars=False)
    assert User(email=email, hashed_password=password) is not None


def test_invalid_email_register() -> None:
    """
    GIVEN an invalid email for user details
    WHEN a new user is created
    THEN check that the new account is NOT created.
    """
    email = faker_data.first_name()
    password = faker_data.password(length=10, special_chars=False)
    with pytest.raises(ValueError):
        assert User(email=email, hashed_password=password) is None


def test_invalid_password_register() -> None:
    """
    GIVEN an invalid password for user details
    WHEN a new user is created
    THEN check that the new account is NOT created.
    """
    email = faker_data.first_name()
    password = faker_data.password(length=10, special_chars=True)
    with pytest.raises(ValueError):
        assert User(email=email, hashed_password=password) is None

