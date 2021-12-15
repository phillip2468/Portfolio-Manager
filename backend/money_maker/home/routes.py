import datetime

import flask
from flask import Blueprint, current_app as app, jsonify
import aiohttp
import asyncio
import requests
from typing import get_type_hints

home_bp = Blueprint('home_bp', __name__)

# https://www.marketindex.com.au/api/v1/companies




def get_aus_tickers() -> requests.Response:
    response: requests.Response = requests.get('https://www.marketindex.com.au/api/v1/companies', headers=header)
    return response.json()


@home_bp.route('/aus_tickers', methods=['GET'])
def these_tickers() -> flask.Response:
    return jsonify(get_aus_tickers())


@home_bp.route('/', methods=['GET'])
def homepage() -> str:
    return 'im the home page!'
