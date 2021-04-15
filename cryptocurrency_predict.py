import numpy as np
from tensorflow import keras
from util import csv_to_dataset, history_points

from binance.client import Client
from binance.enums import *

model = keras.models.load_model('./save_model')

ohlcv_histories, technical_indicators, next_day_open_values, unscaled_y, y_normaliser = csv_to_dataset(symbol="BNBUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, start_time=1618419600000)

test_split = 0.4
n = int(ohlcv_histories.shape[0] * test_split)

ohlcv_train = ohlcv_histories[:n]
tech_ind_train = technical_indicators[:n]
y_train = next_day_open_values[:n]

ohlcv_test = ohlcv_histories[n:]
tech_ind_test = technical_indicators[n:]
y_test = next_day_open_values[n:]

unscaled_y_test = unscaled_y[n:]

y_test_predicted = model.predict([ohlcv_test, tech_ind_test])
y_test_predicted = y_normaliser.inverse_transform(y_test_predicted)

start = 0
end = -1

import matplotlib.pyplot as plt

"""
plt.gcf().set_size_inches(22, 15, forward=True)

real = plt.plot(unscaled_y_test[start:end], label='real')
pred = plt.plot(y_test_predicted[start:end], label='predicted')

plt.legend(['Real', 'Predicted'])

plt.show()
"""

plt.plot(unscaled_y_test, 'b')
plt.plot(y_test_predicted, 'r.')
plt.show()