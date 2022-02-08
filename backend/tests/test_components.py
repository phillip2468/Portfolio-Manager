import pytest
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
    new_user_2 = mixer.blend(User)
    print(new_user_2.hashed_password)
    db.session.add(new_user_2)
    db.session.commit()
    new_user = User(email="asdasdasddas@gmail.com", hashed_password='1234567890')
    print(new_user.email)
    db.session.add(new_user)
    db.session.commit()
    assert len(db.session.query(User).all()) != 0
