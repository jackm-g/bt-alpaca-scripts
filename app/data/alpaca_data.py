import alpaca_trade_api as tradeapi
import threading
import time
import datetime
import os
import csv
import getopt
import sys
import numpy as np
import pandas as pd


API_ID = os.environ.get('API_ID')
API_SECRET = os.environ.get('API_SECRET')
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

class AlpacaData:
    def __init__(self):
        self.alpaca = tradeapi.REST(API_ID, API_SECRET, APCA_API_BASE_URL, 'v2')

    def _get_90days_df(self, symbol):
        barset = self.alpaca.get_barset(symbol, 'day', 90)
        print("Type of barset is {}".format(type(barset)))
        print(type(barset[symbol]))

    def get_1000days_df(self, symbol):
        """
        Get the last 1000 days of a stock's ohlc

        Args:
          symbol: i.e. 'NET'
        Returns:
          dataframe of last 1000 days of ohlc for symbol
        """
        barset = self.alpaca.get_barset(symbol, 'day', 1000)
        return barset.df[symbol]

    def create_d_stock_csv(self, symbol, days):
        results = self.alpaca.get_barset(symbol, 'day', days)
        with open('{}_{}.csv'.format(symbol, days), 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['datetime', 'open', 'high', 'low', 'close', 'volume'])
            for bar in results[symbol]:
                date = bar.t.to_pydatetime().strftime('%Y-%m-%d')
                csv_writer.writerow([date, bar.o, bar.h, bar.l, bar.c, bar.v])
        return '{}_{}.csv'.format(symbol, days)


def main():
    usage_string = 'python {} -s <symbol> -d <days>'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:d:')
    except getopt.GetoptError as err:
        print(err)
        print(usage_string.format(sys.argv[0]))
        sys.exit(2)

    required = ['-s', '-d']
    for option in required:
        if option not in [i[0] for i in opts]:
            print(usage_string.format(sys.argv[0]))
            return

    for o,a in opts:
        if o == '-s':
            symbol = a
        elif o == '-d':
            days = a

    ad = AlpacaData()
    ad.create_d_stock_csv(symbol, days)
    print('Created {}_{}.csv'.format(symbol, days))

if __name__ == "__main__":
    main()