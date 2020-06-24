import alpaca_backtrader_api
import backtrader as bt
from datetime import datetime
from app.data.alpaca_data import AlpacaData
import os
import getopt
import sys

ALPACA_API_KEY = os.environ.get('API_ID')
ALPACA_SECRET_KEY = os.environ.get('API_SECRET')
ALPACA_PAPER = True

store = alpaca_backtrader_api.AlpacaStore(
    key_id=ALPACA_API_KEY,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER
)


class MacdAlpacaStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.macd = bt.indicators.MACDHisto(self.datas[0])
        self.order = None

    def notify_order(self, order):
        print('Callback: notify_order')
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            print(order.status)
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):

        if check_date(self.datas[0].datetime.date(0)):
            print('Current date reached')

            # Check if an order is pending ... if yes, we cannot send a 2nd one
            if self.order:
                print("Order pending, returning")
                return

            # Check if we are in the market
            if not self.position:
                print('No position, checking for buy signal')
                # Check if we should buy: MACD
                if (self.macd[0] > self.macd.signal[0]) and (self.macd[-1] < self.macd.signal[-1]):
                    self.log('MACD crossed above, buy signal')
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy(data=self.datas[0], size=3, exectype=bt.Order.Market)
                else:
                    print('No buy signal at this time')
            else:
                print('Already have position in market, checking for sell signal')
                if (self.macd[0] < self.macd.signal[0]) and (self.macd[-1] > self.macd.signal[-1]):
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])
                    self.order = self.sell()
                else:
                    print('No sell signal at this time')


def check_date(bt_date):
    current_date = datetime.today().strftime('%Y-%m-%d')
    if current_date == str(bt_date):
        return True
    return False


def trade(ticker):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MacdAlpacaStrategy)
    broker = store.getbroker()  # or just alpaca_backtrader_api.AlpacaBroker()
    cerebro.setbroker(broker)

    try:
        ad = AlpacaData()
        csv_file = ad.create_d_stock_csv(ticker, 90)
    except Exception as e:
        print('Issue with alpaca_data:')
        print(e)
        exit(2)

    data = bt.feeds.GenericCSVData(
        headers=True,
        dataname=csv_file,
        dtformat='%Y-%m-%d',
        datetime=0,
        high=1,
        low=2,
        open=3,
        close=4,
        volume=5,
        openinterest=-1
    )
    cerebro.adddata(data)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()


if __name__ == '__main__':
    trade()
