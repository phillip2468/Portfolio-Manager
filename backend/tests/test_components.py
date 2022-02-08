import pytest
from faker import Faker
from money_maker.app import create_test_app
from money_maker.extensions import db, mixer
from money_maker.models.user import User


@pytest.fixture
def setup_database():
    test_app = create_test_app()

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.drop_all()
        db.session.rollback()


def testing_app(setup_database):
    fake_data = Faker()
    email_address = fake_data.ascii_email()
    password = fake_data.password(length=10, special_chars=True)
    print(email_address)
    print(password)
    new_user_2 = mixer.blend(User, email=email_address)
    print(new_user_2.hashed_password)
    db.session.add(new_user_2)
    db.session.commit()
    assert len(db.session.query(User).all()) != 0
