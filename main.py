import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import fetch_data as fd


if __name__ == '__main__':
    prices = fd.get_price_history('SPY')
    prices = fd.remove_date_intervals(prices, 10)
    cash_flows = fd.get_cash_flows('AAPL')
    income_statement = fd.get_income_statement('AAPL')
    balance_sheet = fd.get_balance_sheet('AAPL')
    print(cash_flows)
    print(income_statement)
    print(balance_sheet)



