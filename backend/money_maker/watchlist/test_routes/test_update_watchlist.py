from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE, UPDATE_WATCHLIST_MSG, cleanup_wl_db, NUMBER_OF_WATCHLISTS, CREATE_WATCHLIST_MSG, \
    LOGIN_SUCCESS_MSG
from money_maker.extensions import db
from money_maker.models.watchlist import Watchlist

updated_name = {
    "watchlist_name": "new_name"
}


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

    response = flask_application.patch(f"""/watchlist/{user_id}/{sample_watchlist}""", json=updated_name)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_WATCHLIST_MSG

    assert len(db.session.query(Watchlist).filter(Watchlist.user_id == user_id,
                                                  Watchlist.watchlist_name == updated_name["watchlist_name"]
                                                  ).all()) == 1
    cleanup_wl_db(user_id)


def test_update_one_watchlist_name(flask_application: FlaskClient, user_id: int) -> None:
    """
    GIVEN a valid watchlist name
    WHEN a registered user has multiple watchlists and changes one watchlist name
    THEN check that the watchlist is updated

    Args:
        flask_application: The flask application
        user_id: The id of the user

    """
    for i in range(0, NUMBER_OF_WATCHLISTS):
        response = flask_application.post(f"""/watchlist/{user_id}/sample_watchlist_{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == CREATE_WATCHLIST_MSG

    response = flask_application.patch(f"""/watchlist/{user_id}/sample_watchlist_0""", json=updated_name)
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == UPDATE_WATCHLIST_MSG

    assert len(db.session.query(Watchlist).filter(Watchlist.user_id == user_id,
                                                  Watchlist.watchlist_name == updated_name["watchlist_name"]
                                                  ).all()) == 1

    assert len(db.session.query(Watchlist).filter(Watchlist.user_id == user_id,
                                                  Watchlist.watchlist_name != updated_name["watchlist_name"]
                                                  ).all()) == NUMBER_OF_WATCHLISTS - 1
    cleanup_wl_db(user_id)


def test_invalid_update_watchlist(flask_application: FlaskClient, user_accounts: list[dict]) -> None:
    """
    GIVEN another user from the registered users list
    WHEN this user attempts to update a watchlist for another user
    THEN check that the server responds with an error and that the watchlist remains

    Args:
        flask_application: The flask application
        user_accounts: The list of registered users
        
    """
    response = flask_application.post("/auth/login", json=user_accounts[0])
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == LOGIN_SUCCESS_MSG

    response = flask_application.get("/auth/which_user")
    assert response.status_code == HTTP_SUCCESS_CODE
    user_id = response.get_json()["user_id"]

    response = flask_application.post(f"""/watchlist/{user_id}/sample_watchlist""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == CREATE_WATCHLIST_MSG

    response = flask_application.post("/auth/login", json=user_accounts[1])
    assert response.status_code == HTTP_SUCCESS_CODE
    assert response.get_json()["msg"] == LOGIN_SUCCESS_MSG

    response = flask_application.patch(f"""/watchlist/{user_id}/sample_watchlist""", json=updated_name)
    assert response.status_code != HTTP_SUCCESS_CODE

    assert db.session.query(Watchlist).filter(Watchlist.user_id == user_id,
                                              Watchlist.watchlist_name == "sample_watchlist")\
        .one_or_none() is not None

    cleanup_wl_db(user_id)
