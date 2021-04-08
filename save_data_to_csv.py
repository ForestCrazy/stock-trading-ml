import requests
import datetime
import calendar
import time
import csv
import numpy

from win10toast import ToastNotifier

from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import json
import argparse

"""
def save_dataset(symbol, time_window):
    api_key = '5KDAR88AAANK32GX'
    print(symbol, time_window)
    ts = TimeSeries(key=api_key, output_format='pandas')

    if time_window == 'intraday':
        data, meta_data = ts.get_intraday(
            symbol='MSFT', interval='1min', outputsize='full')
    elif time_window == 'daily':
        data, meta_data = ts.get_daily(symbol, outputsize='full')
    elif time_window == 'daily_adj':
        data, meta_data = ts.get_daily_adjusted(symbol, outputsize='full')

    pprint(data.head(10))

    data.to_csv(f'./{symbol}_{time_window}.csv')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('symbol', type=str, help="the stock symbol you want to download")
    parser.add_argument('time_window', type=str, choices=[
                        'intraday', 'daily', 'daily_adj'], help="the time period you want to download the stock history for")

    namespace = parser.parse_args()
    save_dataset(**vars(namespace))
"""

def crypto_data(symbol, interval, start_time_input, stop_time_input):
    toaster = ToastNotifier()
    data_list = []
    null_data = 0
    time_null_data = None

    def check_interval_level(interval):
        switcher = {
            '1m' : 60,
            '3m' : 120,
            '5m' : 300,
            '15m' : 900,
            '30m' : 1800,
            '1h' : 3600,
            '2h' : 7200,
            '4h' : 14400,
            '6h' : 21600,
            '8h' : 28800,
            '12h' : 43200,
            '1d' : 86400,
            '3d' : 259200,
            '1w' : 604800,
            '1M' : 2592000
        }

        return switcher.get(interval, 4)

    def request_kline_data(start_time, end_time):
        print('happy')

    end_time = int(time.mktime(datetime.datetime.strptime(start_time_input, '%d-%m-%y %H:%M:%S').timetuple()))
    stop_time = int(time.mktime(datetime.datetime.strptime(stop_time_input, '%d-%m-%y %H:%M:%S').timetuple()))
    start_time = end_time
    # end_time = int(time.mktime(datetime.strptime(start_time_input, f'%d/%m/%y {"%H" if check_interval_level(interval) <= 43200}{":%M" if check_interval_level(interval) <= 3600 else ""}')))
    while True:
        time_jump_step = check_interval_level(interval, )
        if end_time >= stop_time:
            break
        if null_data > 2:
            toaster.show_toast("Crypto Price Predicted Project", f"kline data after {time_null_data} is missing.", icon_path=None, duration=10)
            break
        for t in range(1, 1000+1):
            end_time += time_jump_step
            if end_time >= stop_time:
                break

        print(datetime.datetime.fromtimestamp(int(start_time)).strftime('%Y-%m-%d %H:%M:%S'), start_time)
        print(datetime.datetime.fromtimestamp(int(end_time)).strftime('%Y-%m-%d %H:%M:%S'), end_time)
        url = "https://api2.binance.com/api/v3/klines?symbol=" + symbol + "&interval=" + interval + "&limit=1000&startTime=" + str(start_time * 1000) + "&endTime=" + str(end_time * 1000)
        response = ''
        while response == '':
            try:
                response = requests.get(url, headers={'Cache-Control': 'no-cache'})
                for i in response.json():
                    print(datetime.datetime.fromtimestamp(int(i[0]) / 1000).strftime('%Y-%m-%d %H:%M:%S'))
                    print('Open : ', i[1])
                    print('Close : ', i[4])
                    print('High : ', i[2])
                    print('Low : ', i[3])
                    print('Volume : ', i[5])
                    print('\n')
                    data_list.insert(0, [datetime.datetime.fromtimestamp(int(i[0]) / 1000).strftime('%Y-%m-%d %H:%M:%S'), i[1], i[4], i[2], i[3], i[5]])
                if not response.json():
                    null_data += 1
                    if time_null_data == None:
                        time_null_data = datetime.datetime.fromtimestamp(int(end_time)).strftime('%Y-%m-%d %H:%M:%S')
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue
        start_time = end_time + time_jump_step
    toaster.show_toast("Crypto Price Predicted Project", f"success load all kline data from {datetime.datetime.strptime(start_time_input, '%d-%m-%y %H:%M:%S')} to {datetime.datetime.strptime(stop_time_input, '%d-%m-%y %H:%M:%S')}.", icon_path=None, duration=10)

    if data_list:
        ## init csv file
        a = numpy.array([['date','1. open','2. high','3. low','4. close','5. volume']])
        with open(symbol + '.csv', 'a', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(a)

        for data in data_list:
            a = numpy.array([data])

            with open(symbol + '.csv', 'a', newline='') as file:
                mywriter = csv.writer(file, delimiter=',')
                mywriter.writerows(a)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('symbol', type=str, help="the stock symbol you want to download")
    parser.add_argument('interval', type=str, choices=['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'], help="the stock symbol you want to download")
    parser.add_argument('start_time_input', type=str, help="the start year kline data you want to download")
    parser.add_argument('stop_time_input', type=str, help="the end year kline data you want to download")

    namespace = parser.parse_args()
    crypto_data(**vars(namespace))