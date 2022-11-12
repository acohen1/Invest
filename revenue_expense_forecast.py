import fetch_data as fd
import pandas as pd
import numpy as np
import datetime


def generate_dataframe(symbol, year_lower_bound, year_upper_bound):
    """
    WARNING: current year_lower_bound is limited to 3 years before current year (IEX cloud api limitation)
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
    income_statement = fd.get_income_statement(symbol)

    #parse income statements from lower bound to current year and set values in rev_exp_forecast
    for year in range(year_lower_bound, current_year+1):
        rev_exp_forecast.loc['Revenue', year] = income_statement[year-current_year]['totalRevenue']
        rev_exp_forecast.loc['COGS', year] = income_statement[year-current_year]['costOfRevenue']
        rev_exp_forecast.loc['SG&A', year] = income_statement[year-current_year]['sellingGeneralAndAdmin']
        rev_exp_forecast.loc['R&D', year] = income_statement[year-current_year]['researchAndDevelopment']
        rev_exp_forecast.loc['Net Interest', year] = income_statement[year-current_year]['interestIncome']
        rev_exp_forecast.loc['Other income/expenses', year] = income_statement[year-current_year]['otherIncomeExpenseNet']
        rev_exp_forecast.loc['Tax Expense', year] = income_statement[year-current_year]['incomeTax']
        rev_exp_forecast.loc['Net Profit', year] = income_statement[year-current_year]['netIncome']


    return rev_exp_forecast