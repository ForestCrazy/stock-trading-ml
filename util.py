import pandas as pd
from sklearn import preprocessing
import numpy as np

from binance.client import Client
from binance.enums import *

history_points = 20


def csv_to_dataset(**options):
    """
    :param csv_path: path/to/csv/file
    :type csv_path: str
    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Binance Kline interval
    :type interval: str
    :param start_time: Start date string in UTC format or timestamp in milliseconds
    :type start_time: str|int
    :param end_time: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
    :type end_time: str|int
    """
    if options.get('csv_path') == None:
        if None in {options.get('symbol'), options.get('interval'), options.get('start_time')}:
            raise Exception("argument requires")
        else:
            symbol = options.get('symbol')
            interval = options.get('interval')
            start_time = options.get('start_time')
            if options.get('end_time'):
                end_time = options.get('end_time')
            else:
                end_time = None
        
        api_key = ''
        api_secret = ''
        client = Client(api_key, api_secret)

        candles = client.get_historical_klines(symbol, interval, start_time, end_time)

        data = pd.DataFrame(candles)
        
        data.rename(columns={1 : 'Open', 2 : 'High', 3 : 'Low', 4 : 'Close', 5 : 'Volume'}, inplace=True)

        
        data = data.drop([0, 6, 7, 8, 9, 10, 11], axis=1)
        data = data.drop(0, axis=0)

        data['Open'] = data['Open'].astype('float')
        data['High'] = data['High'].astype('float')
        data['Low'] = data['Low'].astype('float')
        data['Close'] = data['Close'].astype('float')
        data['Volume'] = data['Volume'].astype('float')
        
        # print(data.to_string())
    else :
        data = pd.read_csv(options.get('csv_path'))
        data = data.drop('date', axis=1)
        data = data.drop(0, axis=0)

    data = data.values

    data_normaliser = preprocessing.MinMaxScaler()
    data_normalised = data_normaliser.fit_transform(data)

    # using the last {history_points} open close high low volume data points, predict the next open value
    ohlcv_histories_normalised = np.array([data_normalised[i:i + history_points].copy() for i in range(len(data_normalised) - history_points)])
    next_day_open_values_normalised = np.array([data_normalised[:, 0][i + history_points].copy() for i in range(len(data_normalised) - history_points)])
    next_day_open_values_normalised = np.expand_dims(next_day_open_values_normalised, -1)

    next_day_open_values = np.array([data[:, 0][i + history_points].copy() for i in range(len(data) - history_points)])
    next_day_open_values = np.expand_dims(next_day_open_values, -1)

    y_normaliser = preprocessing.MinMaxScaler()
    y_normaliser.fit(next_day_open_values)

    def calc_ema(values, time_period):
        # https://www.investopedia.com/ask/answers/122314/what-exponential-moving-average-ema-formula-and-how-ema-calculated.asp
        sma = np.mean(values[:, 3])
        ema_values = [sma]
        k = 2 / (1 + time_period)
        for i in range(len(his) - time_period, len(his)):
            close = his[i][3]
            ema_values.append(close * k + ema_values[-1] * (1 - k))
        return ema_values[-1]

    technical_indicators = []
    for his in ohlcv_histories_normalised:
        # note since we are using his[3] we are taking the SMA of the closing price
        sma = np.mean(his[:, 3])
        macd = calc_ema(his, 12) - calc_ema(his, 26)
        technical_indicators.append(np.array([sma]))
        # technical_indicators.append(np.array([sma,macd,]))

    technical_indicators = np.array(technical_indicators)

    tech_ind_scaler = preprocessing.MinMaxScaler()
    technical_indicators_normalised = tech_ind_scaler.fit_transform(technical_indicators)

    assert ohlcv_histories_normalised.shape[0] == next_day_open_values_normalised.shape[0] == technical_indicators_normalised.shape[0]
    return ohlcv_histories_normalised, technical_indicators_normalised, next_day_open_values_normalised, next_day_open_values, y_normaliser


def multiple_csv_to_dataset(test_set_name):
    import os
    ohlcv_histories = 0
    technical_indicators = 0
    next_day_open_values = 0
    for csv_file_path in list(filter(lambda x: x.endswith('daily.csv'), os.listdir('./'))):
        if not csv_file_path == test_set_name:
            print(csv_file_path)
            if type(ohlcv_histories) == int:
                ohlcv_histories, technical_indicators, next_day_open_values, _, _ = csv_to_dataset(csv_file_path)
            else:
                a, b, c, _, _ = csv_to_dataset(csv_file_path)
                ohlcv_histories = np.concatenate((ohlcv_histories, a), 0)
                technical_indicators = np.concatenate((technical_indicators, b), 0)
                next_day_open_values = np.concatenate((next_day_open_values, c), 0)

    ohlcv_train = ohlcv_histories
    tech_ind_train = technical_indicators
    y_train = next_day_open_values

    ohlcv_test, tech_ind_test, y_test, unscaled_y_test, y_normaliser = csv_to_dataset(test_set_name)

    return ohlcv_train, tech_ind_train, y_train, ohlcv_test, tech_ind_test, y_test, unscaled_y_test, y_normaliser
