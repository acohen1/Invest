import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import datetime
import fetch_data as fd
import revenue_expense_forecast as md
import revenue_expense_forecast as ref


if __name__ == '__main__':

    current_year = datetime.date.today().year
    rf = ref.generate_dataframe('AAPL', 2017, 2025)

    raw_data = fd.get_raw_financials('AAPL', current_year - 2017 + 1)
    income_statement = fd.get_income_statement('AAPL')
    cash_flows = fd.get_cash_flows('AAPL')
    balance_sheet = fd.get_balance_sheet('AAPL')

    print(rf)



