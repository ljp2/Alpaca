import os

from datetime import datetime, time, timedelta

import pytz
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient

apikey = 'PKKJZYB9P6Q36H84YMXF'
secretkey = 'hBnEAEiD1f67p6hM4DKkUBtixY01YulNWSuGHOyx'

def getBarsDirectory():
    if os.name == "nt":
        BARS1_DIRECTORY = "C:/Alpaca/Data/bars1"
    else:
        BARS1_DIRECTORY = "/Users/ljp2/Alpaca/Data/bars1"
    return BARS1_DIRECTORY


def get_most_current_file_date(dir_name):
    s = max(os.listdir(dir_name)).split('.')[0]
    d = datetime.strptime(s, '%Y%m%d')
    return d.strftime("%Y-%m-%d")


BARS1_DIRECTORY = getBarsDirectory()

trading_client = TradingClient(apikey, secretkey, paper=True)
stock_hist_client = StockHistoricalDataClient(apikey, secretkey)

today = datetime.today()
dd = timedelta(days=1)
if today.time() < time(18, 0):
    startday = today.date() - dd
else:
    startday = today.date()

query_time_start = datetime(startday.year, startday.month, startday.day, 14, 30)
most_current_file_date = get_most_current_file_date(BARS1_DIRECTORY)

for i in range(300):
    queryTime = query_time_start - i * dd
    if queryTime.strftime("%Y-%m-%d") == most_current_file_date:
        break

    weekday = queryTime.weekday()
    if weekday <= 4:
        print(queryTime, weekday,
              ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][weekday])

        request_params = StockBarsRequest(
            symbol_or_symbols='SPY',
            timeframe=TimeFrame.Minute,
            start=queryTime.strftime("%Y-%m-%d 14:30"),
            end=queryTime.strftime("%Y-%m-%d 20:59")
        )
        try:
            bars = stock_hist_client.get_stock_bars(request_params)['SPY']
            fname = f'{queryTime.strftime("%Y%m%d")}.csv'
            f = open(f'{BARS1_DIRECTORY}/{fname}', 'w')
            f.write("time,open,high,low,close,volume,wap\n")
            for b in bars:
                t = b.timestamp.astimezone(pytz.timezone('US/Eastern')).strftime('%H:%M:%S')
                f.write(f"{t},{b.open}, {b.high},{b.low},{b.close},{b.volume},{b.vwap:.3f}\n")
            f.close()
        except:
            print('Possible Holiday')

print("DONE")