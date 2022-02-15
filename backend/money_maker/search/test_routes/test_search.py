from flask.testing import FlaskClient

from conftest import HTTP_SUCCESS_CODE


def test_valid_search_term(flask_application: FlaskClient) -> None:
    """
    GIVEN a string search term
    WHEN a user attempts to search for companies
    THEN return the resulting list of that search will be returned.
    Args:
        flask_application: The flask application

    """
    search_term = "aa"
    response = flask_application.get(f"""/search/{search_term}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(response.get_json()) == 4


def test_valid_search_by_company_ticker(flask_application: FlaskClient) -> None:
    """
    GIVEN a valid ticker symbol (in this case Apple)
    WHEN a user attempts to search with this search term
    THEN return only one result of this company.

    Args:
        flask_application: The flask application

    """
    search_term = "AAPL"
    response = flask_application.get(f"""/search/{search_term}""")
    assert response.status_code == HTTP_SUCCESS_CODE
    assert len(response.get_json()) == 1
    apple_stock = response.get_json()[0]
    assert apple_stock["stock_name"] == "Apple Inc."
    assert apple_stock["symbol"] == "AAPL"


def test_invalid_empty_search(flask_application: FlaskClient) -> None:
    """
    GIVEN an invalid search term
    WHEN the user attempts to search with an empty string
    THEN return nothing and return a 400 response.

    Args:
        flask_application: The flask application

    """
    search_term = ""
    response = flask_application.get(f"""/search/{search_term}""")
    assert response.status_code != HTTP_SUCCESS_CODE
