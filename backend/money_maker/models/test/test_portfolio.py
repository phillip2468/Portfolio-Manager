import random

import pytest
from conftest import REPEAT_TESTS
from marshmallow import ValidationError
from money_maker.extensions import faker_data
from money_maker.models.portfolio import Portfolio, portfolio_schema


@pytest.mark.repeat(REPEAT_TESTS)
def test_valid_portfolio_create(user_id: int) -> None:
    """
    GIVEN valid portfolio
    WHEN portfolio needs to be created
    THEN check the portflio can be successfully created
    """
    random_length = random.randint(1, 16)
    pf_data = {
        "portfolio_name": faker_data.lexify(text=random_length*"?"),
        "user_id": user_id
    }
    result = portfolio_schema.load(data=pf_data, partial=True)
    assert result is not None


def test_invalid_portfolio_empty_name_create(user_id: int) -> None:
    """
    GIVEN an invalid portfolio name
    WHEN portfolio needs to be created
    THEN check the portflio CANNOT be successfully created
    """
    with pytest.raises(ValueError):
        pf_data = {
            "portfolio_name": "",
            "user_id": user_id
        }
        assert portfolio_schema.load(pf_data) is None


def test_invalid_portfolio_no_user_create() -> None:
    """
    GIVEN a portfolio
    WHEN a portfolio is created without a user
    THEN check the portfolio is not created
    """
    with pytest.raises(ValidationError):
        random_length = random.randint(1, 16)
        pf = Portfolio(portfolio_name=faker_data.lexify(text=random_length*"?"))
        portfolio_schema.load(pf)
        assert pf is None

