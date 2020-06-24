# bt-alpaca-scripts
Python scripts for backtesting and running algorithmic trades on https://alpaca.markets

# Usage
## Requirements
1. Python package `alpaca_backtrader_api` https://github.com/alpacahq/alpaca-trade-api-python
2. Python package `backtrader` https://www.backtrader.com/docu/installation/

## Manually running
After pip installing the requisite python packages:

1. `$ source alpaca_keys`

    Example `alpaca_keys` file (generate api keys at https://alapaca.markets):
    ```sh
    export API_ID=<alpaca-api-id>
    export API_SECRET=<alpaca-api-secret>
    ```

2. `$ python main.py -t <TICKER>`

    `<TICKER>` can be a stock symbol such as `AAPL` or `FSLY`

## Crontab 
Use crontab to periodically run the python script automatically.