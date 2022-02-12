from conftest import HTTP_SUCCESS_CODE
from money_maker.extensions import db
from money_maker.models.ticker_prices import TickerPrice


def test_stock_info_from_database(flask_application):
    """
    GIVEN a request to check stock information
    WHEN requested this informaiton
    THEN check that the response is successful and that the symbols match
    in the database
    Args:
        flask_application: The flask testing application

    """
    list_of_stocks = db.session.query(TickerPrice).all()
    for stock in list_of_stocks:
        request = flask_application.get(f"""/quote/{stock.symbol}""")
        assert request.status_code == HTTP_SUCCESS_CODE
        assert request.get_json()["symbol"] == stock.symbol


def test_invalid_stock_info_from_database(flask_application):
    request = flask_application.get(f"""/quote/JMNDKLADSAMJKDJMKASDJKMNA12312""")
    print(request.get_json())
    assert request.status_code != HTTP_SUCCESS_CODE