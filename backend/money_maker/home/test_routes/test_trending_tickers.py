from conftest import HTTP_SUCCESS_CODE
from flask.testing import FlaskClient


def test_trending_tickers(flask_application: FlaskClient) -> None:
    """
    GIVEN a request to find out the most actively traded stocks
    WHEN the user indicates a request
    THEN check that a 200 response is returned, with the relevant stocks
    Args:
        flask_application: The flask application
    """
    response = flask_application.get("/actively-traded")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(response.get_json()) == 5
    