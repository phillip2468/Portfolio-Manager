from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, CREATE_WATCHLIST_MSG, NUMBER_OF_WATCHLISTS
from money_maker.extensions import db
from money_maker.models.watchlist import Watchlist

wl_name = "sample_watchlist_"


def test_get_all_watchlists(flask_application: FlaskClient, user_id: int) -> None:
    """
    GIVEN a valid registered user
    WHEN a user requests to get all their watchlists
    THEN return a response containing a list of all their watchlists

    Args:
        flask_application: The flask application
        user_id: The id of the user

    """
    for i in range(0, NUMBER_OF_WATCHLISTS):
        response = flask_application.post(f"""/watchlist/{user_id}/{wl_name}{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == CREATE_WATCHLIST_MSG

    response = flask_application.get(f"""/watchlist/{user_id}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(response.get_json()) == NUMBER_OF_WATCHLISTS

    db.session.query(Watchlist).filter(Watchlist.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()

    assert len(db.session.query(Watchlist.user_id == user_id).all()) == 0


def test_invalid_user_get_all_watchlists(flask_application: FlaskClient, user_accounts: list[dict]) -> None:
    """
    GIVEN another user from the registered users list
    WHEN this user attempts to get all watchlist from the other user
    THEN check that the server responds with an error (since they do not have permission to view other users)

    Args:
        flask_application: The flask application
        user_accounts: The list of registered accounts
        
    """
    response = flask_application.post("/auth/login", json=user_accounts[0])
    assert response.status_code == HTTP_SUCCESS_CODE

    response = flask_application.get("/auth/which_user")
    assert response.status_code == HTTP_SUCCESS_CODE
    user_id = response.get_json()["user_id"]

    for wl in range(0, NUMBER_OF_WATCHLISTS):
        response = flask_application.post(f"""/watchlist/{user_id}/other_pf_{wl}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == CREATE_WATCHLIST_MSG

    assert len(db.session.query(Watchlist).all()) == NUMBER_OF_WATCHLISTS

    response = flask_application.post("/auth/login", json=user_accounts[1])
    assert response.status_code == HTTP_SUCCESS_CODE

    response = flask_application.post(f"""/watchlist/{user_id}""")
    assert response != HTTP_SUCCESS_CODE

    db.session.query(Watchlist).filter(Watchlist.user_id == user_id).delete(synchronize_session="fetch")
    db.session.commit()

    assert len(db.session.query(Watchlist.user_id == user_id).all()) == 0
