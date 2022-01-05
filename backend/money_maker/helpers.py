import requests
from requests import Response
from sqlalchemy import inspect

header: dict[str, str] = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
}


def sync_request(url: str) -> requests.Response:
    """
    Sends a simple synchronous request to the website. Retrieves the data
    as a json.
    :param url: The website link.
    :type url: str
    :return: The response as a json.
    :rtype: requests.Response
    """
    response: requests.Response = requests.get(url, headers=header)
    return response.json()


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def market_index_ticker() -> Response:
    """
    Gets the code, status and title of all ASX listed stocks.
    All results are held in a list of dictionaries.
    code, status, title
    :return: List of dictionaries
    :rtype: list[dict[str, str, str]]
    """
    url: str = 'https://www.marketindex.com.au/api/v1/companies'
    return sync_request(url)