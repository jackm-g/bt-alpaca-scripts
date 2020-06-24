from app.alpaca_trading.macd_trade_alpaca import trade
import getopt
import sys

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 't:')
    except getopt.GetoptError as err:
        print(err)
        print('Usage: python {} -t <TICKER>'.format(sys.argv[0]))
        sys.exit(2)

    required = ['-t']
    for option in required:
        if option not in [i[0] for i in opts]:
            print('Usage: python {} -t <TICKER>'.format(sys.argv[0]))
            exit(1)

    for o, a in opts:
        if o == '-t':
            print(a)
            ticker = a

    trade(ticker)