import datetime

from flask import Blueprint, current_app as app, jsonify
import aiohttp
import asyncio
import requests

home_bp = Blueprint('home_bp', __name__)

# https://www.marketindex.com.au/api/v1/companies

header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
}


def get_aus_tickers() -> requests.Response:
    response: requests.Response = requests.get('https://www.marketindex.com.au/api/v1/companies', headers=header)
    return response.json()


@home_bp.route('/aus_tickers', methods=['GET'])
def these_tickers():
    return jsonify(get_aus_tickers())


@home_bp.route('/', methods=['GET'])
def homepage():
    return 'im the home page!'
