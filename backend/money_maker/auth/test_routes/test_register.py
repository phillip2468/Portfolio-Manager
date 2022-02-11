import random

import pytest
from flask.testing import FlaskClient

from conftest import (HTTP_SUCCESS_CODE, LETTER_CASINGS, MAX_LENGTH_EMAIL,
                      MIN_LENGTH_EMAIL, REPEAT_TESTS)
from money_maker.extensions import db, faker_data
from money_maker.models.user import User


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_register(client: FlaskClient) -> None:
    """
    GIVEN valid user_details
    WHEN a new user registers
    THEN check that the user exists in the database by checking
    the length of rows.

    Args:
        client: The flask application
    """
    body = {
        "email": faker_data.ascii_email(),
        "password": faker_data.password(length=10, special_chars=False)
    }
    response = client.post("/auth/register", json=body)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(db.session.query(User).all()) == 1


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_multiple_register(client: FlaskClient) -> None:
    """
    GIVEN multiple Users
    WHEN each User registers
    THEN check that each user in the database exists by checking
    the length of rows in the database.

    Args:
        client: The flask application

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
def test_invalid_register_email(client: FlaskClient) -> None:
    """
    GIVEN a user with a first name as their email address
    WHEN a User registers
    THEN check that the model raises a valuerror and does not insert the user

    Args:
        client: The flask application

    """

    with pytest.raises(ValueError):
        random_num = random.randint(MIN_LENGTH_EMAIL, MAX_LENGTH_EMAIL)
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
def test_invalid_register_short_pw(client: FlaskClient) -> None:
    """
    GIVEN a user with a password between 4 and 7 characters
    WHEN a User registers
    THEN check that the model raises a valuerror and does not insert the user

    Args:
        client: The flask application

    """
    with pytest.raises(ValueError):
        casing = random.choice(LETTER_CASINGS)
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
def test_invalid_register_passwords(client: FlaskClient) -> None:
    """
    GIVEN a user with a password that contains special characters
    WHEN a User registers
    THEN check that the model raises a valuerror and does not insert the user

    Args:
        client: The flask application
    """

    with pytest.raises(ValueError):
        casing = random.choice(LETTER_CASINGS)
        body = {
            "email": faker_data.ascii_email(),
            "password": faker_data.password(length=random.randint(MIN_LENGTH_EMAIL, MAX_LENGTH_EMAIL),
                                            special_chars=True,
                                            digits=random.choice([True, False]),
                                            upper_case=casing[0],
                                            lower_case=casing[1])
        }
        client.post("/auth/register", json=body)
