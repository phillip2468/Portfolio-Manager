import requests
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