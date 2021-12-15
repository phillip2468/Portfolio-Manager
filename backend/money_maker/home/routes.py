import datetime
import typing

import flask
from flask import Blueprint, current_app as app, jsonify
import aiohttp
import asyncio
import requests

from money_maker.helpers import sync_request

home_bp = Blueprint('home_bp', __name__)


def get_aus_tickers() -> list[dict[str, str, str]]:
    """
    Gets the code, status and title of all ASX listed stocks.
    All results are held in a list of dictionaries.
    :return: List of dictionaries
    :rtype: list[dict[str, str, str]]
    """
    url: str = 'https://www.marketindex.com.au/api/v1/companies'
    return sync_request(url)


@home_bp.route('/aus_tickers', methods=['GET'])
def asx_tickers() -> flask.Response:
    """
    Packages the response to a json format.
    :return: The list of dictionaries containing the tickers.
    :rtype: flask.Response
    """
    return jsonify(get_aus_tickers())


@home_bp.route('/', methods=['GET'])
def homepage() -> str:
    return 'im the home page!'
