from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice


def test_get_stock_information(client, symbols):
    """
    GIVEN the flask client
    WHEN a request is submitted to check all stock prices
    THEN check that the stock was successfully inserted into the database (in this case since
    the first 100 stocks are updated AAPL is checked to see if inserted)
    """
    response = client.get("/task")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(db.session.query(TickerPrice).all()) > 1
    assert len(db.session.query(TickerPrice).filter(TickerPrice.symbol == 'AAPL').all()) == 1
