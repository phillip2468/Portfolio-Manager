import keras.models
import numpy as np
import pandas as pd
from flask import Blueprint, jsonify
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import LSTM, Dense, Dropout
from yahooquery import Ticker

import tensorflow as tf
import logging
import os

predictor_bp = Blueprint("predictor_bp", __name__)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


@predictor_bp.route("/ai-data")
def past_data():
    stock = "CBA.AX"
    training_data_prices = Ticker(stock).history(interval="1d", start="2020-01-01", end="2020-6-30")
    test_data_prices = Ticker(stock).history(interval="1d", start="2021-01-01", end="2021-6-30")

    with tf.device('/cpu:0'):
        tf.get_logger().setLevel(logging.ERROR)

        x_values = training_data_prices['close'].values.reshape(-1, 1)

        # Prepare data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(x_values)

        # How many days should I look into the past to predict the next prices?
        prediction_days = 60

        x_train, y_train = [], []
        for x in (prediction_days, len(scaled_data) - 1):
            x_train.append(scaled_data[x - prediction_days: x, 0])
            # This appends the last day after the x prediction days
            y_train.append(scaled_data[x, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # Build the model, neural networks
        if os.path.exists("./models") is False:
            print("HERE")
            model = Sequential()
            # Some-how feeds information back into itself with Long-short term memory???
            model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(Dropout(0.2))
            model.add(LSTM(units=50, return_sequences=True))
            model.add(Dropout(0.2))
            model.add(LSTM(units=50))
            model.add(Dropout(0.2))
            model.add(Dense(units=1))  # Prediction of the next closing value

            model.compile(optimizer='adam', loss='mean_squared_error')
            model.save('./models')

        model: Sequential = keras.models.load_model('./models')

        model.fit(x_train, y_train, epochs=50, batch_size=32, verbose=False)

        # Test the model
        actual_test_data_close = test_data_prices['close'].values

        total_dataset = pd.concat((training_data_prices['close'], test_data_prices['close']), axis=0)

        model_inputs = total_dataset[len(total_dataset) - len(test_data_prices) - prediction_days:].values
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

        model.save('./models')
        dictionary = {
            "actual": [{"day": index, "price": str(element)} for index, element in
                       enumerate(actual_test_data_close.flat)],
            "predicted": [{"day": index, "price": str(element)} for index, element in
                          enumerate(predicted_prices.flat)],
            "next_day": [str(element) for element in prediction.flat]
        }

    return jsonify(dictionary)
