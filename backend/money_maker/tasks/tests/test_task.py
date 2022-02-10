from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice


def test_get_stock_information(client, symbols):
    response = client.get("/task")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(db.session.query(TickerPrice).all()) == 1
