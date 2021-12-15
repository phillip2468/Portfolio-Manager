import datetime
import typing

import flask
from flask import Blueprint, current_app as app, jsonify
import aiohttp
import asyncio
import requests
from requests import Response

from backend.money_maker.helpers import sync_request
from money_maker.celery_tasks.tasks import add_together
from celery.result import AsyncResult

home_bp = Blueprint('home_bp', __name__)


def get_aus_tickers() -> Response:
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


@home_bp.route('/')
def serve():
    result = add_together.delay()
    print(result.wait())
    return app.send_static_file('index.html')


@home_bp.route('/tasks/<task_id>')
def check_task(task_id):
    task = AsyncResult(task_id)

    if task.state == 'FAILURE':
        result = None
        error = str(task.result)
    else:
        result = task.result
        error = None

    response = {
        'id': task_id,
        'state': task.state,
        'result': result,
        'error': error,
    }
    return jsonify(response)
