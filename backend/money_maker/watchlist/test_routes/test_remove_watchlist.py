from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, CREATE_WATCHLIST_MSG, cleanup_wl_db
from money_maker.models.watchlist import Watchlist


def test_remove_watchlist(flask_application: FlaskClient, user_id: int) -> None:
    """
    GIVEN a valid watchlist name
    WHEN a registered user creates a watchlist
    THEN check that the watchlist is created in the backend
    Args:
        flask_application: The flask application
        user_id: The id of the user

    """
    response = flask_application.post(f"""/watchlist/{user_id}/sample_watchlist_1""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == CREATE_WATCHLIST_MSG

    assert len(db.session.query(Watchlist).filter(Watchlist.user_id == user_id).all()) == 1

    cleanup_wl_db(user_id)

