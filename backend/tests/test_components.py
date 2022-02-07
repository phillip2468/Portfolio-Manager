import pytest
from alembic.command import upgrade
from alembic.config import Config
from money_maker.app import create_test_app
from money_maker.models.user import User
from money_maker.test_extensions import test_db

ALEMBIC_CONFIG = 'alembic.ini'


def apply_migrations():
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, 'head')


@pytest.fixture
def setup_database():
    test_app = create_test_app()

    with test_app.app_context():
        test_db.create_all()
        apply_migrations()
        yield test_app
        test_db.drop_all()


def testing_app(setup_database):
    with setup_database.app_context():
        assert (test_db.session.query(User).all() == 90)
