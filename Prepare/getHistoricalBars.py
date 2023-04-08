import os

from datetime import datetime, time, timedelta

import pytz
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient

eastern_timezone= pytz.timezone('US/Eastern')

apikey = 'PKKJZYB9P6Q36H84YMXF'
secretkey = 'hBnEAEiD1f67p6hM4DKkUBtixY01YulNWSuGHOyx'
stock_hist_client = StockHistoricalDataClient(apikey, secretkey)

def isDST(date:datetime):
    return eastern_timezone.localize(date).dst() != timedelta(0)

def getBarsDirectory():
    if os.name == "nt":
        BARS1_DIRECTORY = "C:/Alpaca/Data/bars1"
    else:
        BARS1_DIRECTORY = "/Users/ljp2/Alpaca/Data/bars1"
    return BARS1_DIRECTORY


def get_most_current_file_date(dir_name):
    files = os.listdir(dir_name)
    if len(files) == 0:
        return 'EMPTY'
    else:
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

query_date_start = datetime(startday.year, startday.month, startday.day)
most_current_file_date = get_most_current_file_date(BARS1_DIRECTORY)

for i in range(100):
    queryDate = query_date_start - i * dd
    if queryDate.strftime("%Y-%m-%d") == most_current_file_date:
        break

    weekday = queryDate.weekday()
    if weekday <= 4:
        print(queryDate, weekday,
              ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][weekday])

        if isDST(queryDate):
            request_params = StockBarsRequest(
                symbol_or_symbols='SPY',
                timeframe=TimeFrame.Minute,
                start=queryDate.strftime("%Y-%m-%d 13:30"),
                end=queryDate.strftime("%Y-%m-%d 19:59")
            )
        else:
             request_params = StockBarsRequest(
                symbol_or_symbols='SPY',
                timeframe=TimeFrame.Minute,
                start=queryDate.strftime("%Y-%m-%d 14:30"),
                end=queryDate.strftime("%Y-%m-%d 20:59")
            )           
        try:
            bars = stock_hist_client.get_stock_bars(request_params)['SPY']
            fname = f'{queryDate.strftime("%Y%m%d")}.csv'
            f = open(f'{BARS1_DIRECTORY}/{fname}', 'w')
            f.write("time,open,high,low,close,volume,wap\n")
            for b in bars:
                t = b.timestamp.astimezone(pytz.timezone('US/Eastern')).strftime('%H:%M:%S')
                f.write(f"{t},{b.open}, {b.high},{b.low},{b.close},{b.volume},{b.vwap:.3f}\n")
            f.close()
        except:
            print('Possible Holiday')

print("DONE")