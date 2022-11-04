import numpy as np
import pandas
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import fetch_data as hp


if __name__ == '__main__':
    prices = hp.get_price_history('SPY')
    prices = hp.remove_date_intervals(prices, 10)
    cash_flows = hp.get_cash_flows('AAPL')
    income_statement = hp.get_income_statement('AAPL')
    balance_sheet = hp.get_balance_sheet('AAPL')
    print(cash_flows)
    print(income_statement)
    print(balance_sheet)



