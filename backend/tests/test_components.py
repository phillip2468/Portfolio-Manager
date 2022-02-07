import pytest

from money_maker.app import create_test_app
from money_maker.extensions import db
from money_maker.models.user import User


@pytest.fixture
def setup_database():
    test_app = create_test_app()

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.drop_all()


def testing_app(setup_database):
    new_user = User(email="dasmkldas", hashed_password='1234567890')
    db.session.add(new_user)
    assert (db.session.query(User).filter(User.email == "dasmkldas").first() is not None)
