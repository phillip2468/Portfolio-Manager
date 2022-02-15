from flask.testing import FlaskClient

from conftest import NUMBER_OF_STOCKS, ADD_STOCK_TO_WATCHLIST, HTTP_SUCCESS_CODE, cleanup_wl_db, \
    REMOVE_STOCK_TO_WATCHLIST
from money_maker.extensions import db
from money_maker.models.watchlist import Watchlist


def test_remove_stocks_to_watchlist(flask_application: FlaskClient, user_id: int, sample_watchlist: str) -> None:
    """
    GIVEN a valid watchlist name
    WHEN a registered user adds stocks to a watchlist and then removes all the stocks
    THEN check that the watchlist stocks are in the watchlist

    Args:
        flask_application: The flask application
        user_id: The id of the user
        sample_watchlist: The example watchlist created

    """

    for i in range(1, NUMBER_OF_STOCKS + 1):
        response = flask_application.post(f"""/watchlist/{user_id}/{sample_watchlist}/{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == ADD_STOCK_TO_WATCHLIST

    response = flask_application.get(f"""/watchlist/{user_id}/{sample_watchlist}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(response.get_json()) == NUMBER_OF_STOCKS

    assert len(db.session.query(Watchlist).filter(Watchlist.watchlist_name == sample_watchlist
                                                  ).all()) == NUMBER_OF_STOCKS + 1

    for i in range(1, NUMBER_OF_STOCKS + 1):
        response = flask_application.delete(f"""/watchlist/{user_id}/{sample_watchlist}/{i}""")
        assert response.status_code == HTTP_SUCCESS_CODE
        assert response.get_json()["msg"] == REMOVE_STOCK_TO_WATCHLIST

    assert len(db.session.query(Watchlist).filter(Watchlist.watchlist_name == sample_watchlist
                                                  ).all()) == 1

    cleanup_wl_db(user_id)