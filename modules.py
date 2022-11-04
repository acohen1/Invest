import fetch_data as fd
import pandas as pd
import numpy as np


def get_rev_exp_forecast(symbol):
    balance_sheet = fd.get_balance_sheet(symbol)
    income_statement = fd.get_income_statement(symbol)
    cash_flows = fd.get_cash_flows(symbol)

    # TODO: add ability to customise columns to fit arbitrary needs for forecast
    df_columns = ['Revenue', '% Growth', 'COGS', '% of Revenue', 'SG&A', '% of Revenue', 'R&D', '% of Revenue']

