import fetch_data as fd
import pandas as pd
import numpy as np
import datetime


def generate_dataframe(symbol, year_lower_bound, year_upper_bound):
    """
    :param symbol: stock symbol as string
    :param year_upper_bound: upper bound on range for years to generate (int)
    :param year_lower_bound: lower bound on range for years to generate (int)
    :return: empty dataframe with revenue expense formatting
    """
    # generate index and columns for rev exp forecast dataframe
    df_index = [
        'Revenue', '% Growth',
        'COGS', '% of Revenue',
        'SG&A', '% of Revenue',
        'R&D', '% of Revenue',
        'Net Interest', '% of Revenue',
        'Other income/expenses', '% of Revenue',
        'Tax Expense', 'Tax Rate',
        'Net Profit', '% Margin'
    ]
    df_columns = []
    current_year = datetime.date.today().year

    for year in range(year_lower_bound - current_year, year_upper_bound - current_year+1):
        df_columns.append(current_year + year)

    rev_exp_forecast = pd.DataFrame(index=df_index, columns=df_columns)


    # TODO: enter values into rev exp forecast df
    raw_financial_data = fd.get_raw_financials(symbol, current_year-year_lower_bound+1)

    return rev_exp_forecast