from flask import Blueprint, current_app as app, jsonify
import aiohttp
import asyncio

home_bp = Blueprint('home_bp', __name__)

# https://www.marketindex.com.au/api/v1/companies

header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
}
loop = asyncio.get_event_loop()


async def get_aus_tickers():
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get('https://www.marketindex.com.au/api/v1/companies') as response:
            print(response.status)
            return await response.json()


@home_bp.route('/', methods=['GET'])
def homepage():
    results = loop.run_until_complete(get_aus_tickers())
    print(results)
    return jsonify(results)
