import requests
import datetime
import calendar
import time
import csv
import numpy

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

symbol = 'BNB'

## init csv file
a = numpy.array([['date','1. open','2. high','3. low','4. close','5. volume']])
with open(symbol + 'USDT.csv', 'a', newline='') as file:
    mywriter = csv.writer(file, delimiter=',')
    mywriter.writerows(a)

data_list = []

for j in range(1, 12+1):
    _, num_days = calendar.monthrange(2020, j)
    for day in range(1, num_days+1):
        for hour in range(1, 23):
            start_time = int(time.mktime(datetime.datetime(2020, j, day, hour, 0+1, 0).timetuple())) * 1000
            end_time = int(time.mktime(datetime.datetime(2020, j, day, hour+1, 0, 0).timetuple())) * 1000
            url = "https://api2.binance.com/api/v3/klines?symbol=" + symbol + "USDT&interval=1m&limit=1000&startTime=" + str(start_time) + "&endTime=" + str(end_time)
            print(url)
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
                    break
                except:
                    print("Connection refused by the server..")
                    print("Let me sleep for 5 seconds")
                    print("ZZzzzz...")
                    time.sleep(2)
                    print("Was a nice sleep, now let me continue...")
                    continue

for data in data_list:
    a = numpy.array([data])

    with open(symbol + 'USDT.csv', 'a', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(a)