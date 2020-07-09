import alpaca_trade_api
import os

store = alpaca_trade_api.REST()

if store.get_clock().is_open:
    print('market is open')
else:
    print('market is close')
