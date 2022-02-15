from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, UPDATE_WATCHLIST_MSG, cleanup_wl_db
from money_maker.extensions import db
from money_maker.models.watchlist import Watchlist


def test_update_watchlist_name(flask_application: FlaskClient, user_id: int, sample_watchlist: str) -> None:
    """
    GIVEN a valid watchlist name
    WHEN a registered user creates a watchlist
    THEN check that the watchlist is created in the backend
    Args:
        flask_application: The flask application
        user_id: The id of the user
        sample_watchlist: The example watchlist created

    """
    updated_name = {
        "watchlist_name": "new_name"
    }
    response = flask_application.patch(f"""/watchlist/{user_id}/{sample_watchlist}""", json=updated_name)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_WATCHLIST_MSG

    assert len(db.session.query(Watchlist).filter(Watchlist.user_id == user_id,
                                                  Watchlist.watchlist_name == "new_name"
                                                  ).all()) == 1
    cleanup_wl_db(user_id)
