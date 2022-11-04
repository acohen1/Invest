import fetch_data as fd
import pandas as pd
import numpy as np
import datetime


def generate_dataframe():
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
    # 3 years historical; 6 years future
    for year in range(-3, 6):
        df_columns.append(current_year + year)

    rev_exp_forecast = pd.DataFrame(index=df_index, columns=df_columns)
    return rev_exp_forecast


def fill_dataframe(df, symbol):
    # retrieve financials
    # reminder: financial statement functions return list of dictionaries in descending order
    balance_sheet = fd.get_balance_sheet(symbol)
    income_statement = fd.get_income_statement(symbol)
    cash_flows = fd.get_cash_flows(symbol)
    year = datetime.date.today().year






    df.at['Revenue', year] = income_statement['totalRevenue']
    df.at['COGS', year] = income_statement['costOfRevenue']
    df.at['SG&A', year] = income_statement['sellingGeneralAndAdmin']
    df.at['R&D', year] = income_statement['researchAndDevelopment']
    df.at['Net Interest', year] = income_statement['interestIncome']
    df.at['Other income/expenses', year] = income_statement['otherIncomeExpenseNet']
    df.at['Tax Expense', year] = income_statement['incomeTax']
    df.at['Net Profit', year] = income_statement['netIncome']
    return df
