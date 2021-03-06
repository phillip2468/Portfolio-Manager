from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice


def test_refresh_us_stocks(flask_application: FlaskClient) -> None:
    """
    GIVEN a request to refresh US stocks
    WHEN anyone reaches the refresh-us-symbol link and when the TickerPrice database is empty
    THEN check that the database contains at least one row of these stocks
    """
    response = flask_application.get("/ticker/refresh-us-symbols")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(db.session.query(TickerPrice).all()) > 1


def test_refresh_asx_stocks(flask_application: FlaskClient) -> None:
    """
    GIVEN a request to refresh AU stocks
    WHEN anyone reaches the refresh-us-symbol link and when the TickerPrice database is empty
    THEN check that the database contains at least one row of these stocks
    """
    response = flask_application.get("/ticker/refresh-asx-symbols")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(db.session.query(TickerPrice).all()) > 1

