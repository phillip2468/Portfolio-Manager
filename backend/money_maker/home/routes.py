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


async def get_aus_tickers():
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get('https://www.marketindex.com.au/api/v1/companies') as response:
            print(response.status)
            return await response.json()


@home_bp.route('/aus_tickers', methods=['GET'])
async def these_tickers():
    results = await get_aus_tickers()
    return jsonify(results)


@home_bp.route('/', methods=['GET'])
def homepage():
    return 'im the home page!'
