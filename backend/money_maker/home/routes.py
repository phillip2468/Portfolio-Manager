import datetime
import os
import sys
from typing import Any

import flask
import pytz
import yahooquery.ticker
from flask import Blueprint
from flask import current_app as app
from flask import json, jsonify
from money_maker.extensions import db
from money_maker.helpers import market_index_ticker, object_as_dict
from money_maker.models.ticker_prices import TickerPrice
from money_maker.tasks.task import add_together
from sqlalchemy import asc, bindparam, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import ColumnCollection, ColumnElement
from sqlalchemy_utils import get_columns
from yahooquery import Ticker

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

home_bp = Blueprint('home_bp', __name__)


@home_bp.route("/retrieve-asx-tickers")
def asx_tickers() -> flask.Response:
    """
    Inserts asx tickers in the database.
    Returns a list of all tickers.
    """
    print(add_together.delay())

    insert_dictionary: dict[str, ColumnElement[Any]] = {
        'market_state': bindparam('status'),
        'symbol': bindparam('code') + ".AX",
        'stock_name': bindparam('title')
    }

    stmt = insert(TickerPrice).values(insert_dictionary).on_conflict_do_update(
        index_elements=['symbol'],
        set_=insert_dictionary
    )

    db.session.execute(stmt, market_index_ticker())
    db.session.commit()
    result = [object_as_dict(element) for element in (db.session.query(TickerPrice).all())]

    return jsonify(result)


@home_bp.route("/all-asx-prices")
def get_all_asx_prices() -> flask.Response:
    # https://stackoverflow.com/questions/56726689/sqlalchemy-insert-executemany-func
    # https://newbedev.com/sqlalchemy-performing-a-bulk-upsert-if-exists-update-else-insert-in-postgresql

    stmt = select(func.max(TickerPrice.last_updated))
    last_updated_stock = db.session.execute(stmt).one()[0]

    # This is so the database isn't queried every time.
    if pytz.utc.localize(last_updated_stock) + datetime.timedelta(minutes=15) > datetime.datetime.now(pytz.utc):
        return jsonify([object_as_dict(element) for element in db.session.query(TickerPrice).all()])

    list_asx_symbols = select(TickerPrice.symbol).order_by(asc(TickerPrice.symbol))
    list_symbols: list[str] = [element[0] for element in db.session.execute(list_asx_symbols)]

    yh_market_information: yahooquery.Ticker.__dict__ = \
        Ticker(list_symbols, formatted=True, asynchronous=True, max_workers=min(100, len(list_symbols)),
               progress=True,
               country='australia').get_modules('price summaryProfile')

    formatted_yh_information = []
    for element in yh_market_information.values():
        if type(element) == dict and len(element.keys()) == 2:
            raw_dictionary = {**element["price"], **element["summaryProfile"]}
            formatted_yh_information.append({key: value if type(value) != dict else value["raw"] if len(value) > 0
            else None for (key, value) in raw_dictionary.items()})

    market_information = {
        'currency': bindparam('currency', value=None),
        'city': bindparam('city', value=None),
        'industry': bindparam('industry', value=None),
        'zip_code': bindparam('zip', value=None),
        'sector': bindparam('sector', value=None),
        'country': bindparam('country', value=None),
        'exchange': bindparam('exchange', value=None),
        'stock_name': bindparam('longName', value=None),
        'market_cap': bindparam('marketCap', value=None),
        'quote_type': bindparam('quoteType', value=None),
        'market_change': bindparam('regularMarketChange', value=None),
        'market_change_percentage': bindparam('regularMarketChangePercent', value=None),
        'market_high': bindparam('regularMarketDayHigh', value=None),
        'market_low': bindparam('regularMarketDayLow', value=None),
        'market_open': bindparam('regularMarketOpen', value=None),
        'market_previous_close': bindparam('regularMarketPreviousClose', value=None),
        'market_current_price': bindparam('regularMarketPrice', value=None),
        'market_volume': bindparam('regularMarketVolume', value=None),
        'symbol': bindparam('symbol')
    }

    stmt = insert(TickerPrice).values(market_information)

    on_conflict_statement = stmt.on_conflict_do_update(
        index_elements=['symbol'],
        set_=market_information
    )

    db.session.execute(on_conflict_statement, formatted_yh_information)
    db.session.commit()

    return jsonify(formatted_yh_information)


@home_bp.route('/trending-tickers')
def trending_tickers() -> flask.Response:
    """
    Provides a dictionary set of tickers containing
    relevant data to the date. Note that this only returns
    US trending stocks.
    :return: flask.Response
    """
    trending_yh_tickers: dict = yahooquery.get_trending()

    # This gets rid of crypto related items
    trending_securities = [element["symbol"] for element in
                           trending_yh_tickers["quotes"] if "-" not in element["symbol"]]

    data: yahooquery.ticker.Ticker.__dict__ = Ticker(trending_securities).price
    wanted_keys = ['symbol', 'regularMarketPrice', 'regularMarketChange',
                   'regularMarketDayHigh', 'regularMarketDayLow', 'marketCap', 'shortName']

    for key, value in data.items():
        new_dict = {k: value[k] for k in set(wanted_keys) & set(value.keys())}
        data[key] = new_dict

    return jsonify(data)


import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import sklearn.preprocessing
from matplotlib.figure import Figure
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential


@home_bp.route('/past-data')
def past_data():
    original_data_prices = Ticker('CBA.AX').history(interval="1d", start="2020-01-01", end="2020-01-25")
    x_values = original_data_prices['adjclose'].values.reshape(-1, 1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(x_values)

    # How many days should i look into the past to predict the next prices?
    prediction_days = 7

    x_train = []
    y_train = []
    for x in (prediction_days, len(scaled_data) - 1):
        x_train.append(scaled_data[x - prediction_days: x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Build the model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))  # Prediction of the next closing value

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32, verbose=0)

    test_the_data_tickers = Ticker('CBA.AX').history(interval="1d", start="2021-01-01", end="2021-01-25")
    actual_test_data_close = test_the_data_tickers['adjclose'].values

    total_dataset = pd.concat((original_data_prices['adjclose'], test_the_data_tickers['adjclose']), axis=0)

    model_inputs = total_dataset[len(total_dataset) - len(test_the_data_tickers) - prediction_days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.transform(model_inputs)

    # Make predictions via the test data
    x_test = []

    for x in range(prediction_days, len(model_inputs)):
        x_test.append(model_inputs[x - prediction_days: x, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predicted_prices = model.predict(x_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)
    # Predict the next day

    real_data = [model_inputs[len(model_inputs) - prediction_days: len(model_inputs + 1), 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)

    dictionary = {
        "actual": [{"day": index, "price": str(element)} for index, element in enumerate(actual_test_data_close.flat)],
        "predicted": [{"day": index, "price": str(element)} for index, element in enumerate(predicted_prices.flat)],
        "next_day": [str(element) for element in prediction.flat]
    }

    return jsonify(dictionary)


@home_bp.route('/')
def serve():
    return app.send_static_file('index.html')
