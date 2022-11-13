import fetch_data as fd
import pandas as pd
import numpy as np
import datetime


def generate_df(year_lower_bound, year_upper_bound):
    """
    WARNING: current year_lower_bound is limited to 3 years before current year (IEX cloud api limitation)
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
    

    

    #in rev_exp_forecast calculate % of revenue for each expense category
    # TODO: fix this to distinguish between each % of revenue category; current implementation changes all rows to the same value
    for year in range(year_lower_bound, current_year+1):
        for expense_category in ['COGS', 'SG&A', 'R&D', 'Net Interest', 'Other income/expenses']:
            revenue = rev_exp_forecast.loc['Revenue', year]
            rev_exp_forecast.loc['% of Revenue', year] = rev_exp_forecast.loc[f'{expense_category}', year] / revenue


    return rev_exp_forecast


def populate_df(symbol, rev_exp_forecast):
    """
    :param rev_exp_forecast: dataframe with revenue expense formatting (generated by generate_df)
    :return: populated dataframe with revenue expense formatting. parses dictionary data pulled from IEX cloud api
    """
    year_lower_bound = rev_exp_forecast.columns[0]
    year_upper_bound = rev_exp_forecast.columns[-1]
    current_year = datetime.date.today().year
    income_statement = fd.get_income_statement(symbol)

    #parse income statements from lower bound to current year and set values in rev_exp_forecast
    # TODO: create arrays for each revenue expense category and their respective dictionary keys; iterate through them
    for year in range(year_lower_bound, current_year+1):
        rev_exp_forecast.loc['Revenue', year] = income_statement[year-current_year]['totalRevenue']
        rev_exp_forecast.loc['COGS', year] = income_statement[year-current_year]['costOfRevenue']
        rev_exp_forecast.loc['SG&A', year] = income_statement[year-current_year]['sellingGeneralAndAdmin']
        rev_exp_forecast.loc['R&D', year] = income_statement[year-current_year]['researchAndDevelopment']
        rev_exp_forecast.loc['Net Interest', year] = income_statement[year-current_year]['interestIncome']
        rev_exp_forecast.loc['Other income/expenses', year] = income_statement[year-current_year]['otherIncomeExpenseNet']
        rev_exp_forecast.loc['Tax Expense', year] = income_statement[year-current_year]['incomeTax']
        rev_exp_forecast.loc['Net Profit', year] = income_statement[year-current_year]['netIncome']
    
    #calculate %growth for revenue, % margin for net profit, and tax rate
    for year in range(year_lower_bound, year_upper_bound+1):
        # calculate % growth
        if year == year_lower_bound:
            rev_exp_forecast.loc['% Growth', year] = 0
        else:
            rev_exp_forecast.loc['% Growth', year] = rev_exp_forecast.loc['Revenue', year] / rev_exp_forecast.loc['Revenue', year-1] - 1

        # calculate % margin
        rev_exp_forecast.loc['% Margin', year] = rev_exp_forecast.loc['Net Profit', year] / rev_exp_forecast.loc['Revenue', year]

        # calculate tax rate
        rev_exp_forecast.loc['Tax Rate', year] = rev_exp_forecast.loc['Tax Expense', year] / rev_exp_forecast.loc['Net Profit', year]

    # calculate % of revenue for each expense category and set values in rev_exp_forecast. current implementation is an inefficient
    # workaround for the fact that there are multiple % of revenue categories with the same name
    list_of_percent_of_revenue_indices = []
    for idx, row in enumerate(rev_exp_forecast.index):
        if row == '% of Revenue':
            list_of_percent_of_revenue_indices.append(idx)
    for year in range(year_lower_bound, current_year+1):
        revenue = rev_exp_forecast.loc['Revenue', year]
        for index in list_of_percent_of_revenue_indices:
            rev_exp_forecast.iloc[index, year-year_lower_bound] = rev_exp_forecast.iloc[index-1, year-year_lower_bound] / revenue

    return rev_exp_forecast


#using the data generated from populate_df, forecast revenue and expenses for years beyond the current year and below the upper bound
def forecast_df(rev_exp_forecast):
    """
    :param rev_exp_forecast: populated dataframe with revenue expense formatting (generated by populate_df)
    :return: forecasted dataframe with revenue expense formatting
    """
    year_lower_bound = rev_exp_forecast.columns[0]
    year_upper_bound = rev_exp_forecast.columns[-1]
    current_year = datetime.date.today().year

    # forecast revenue and expenses for years beyond the current year and below the upper bound

    #calculate average % growth for the last 3 years
    average_growth_rate = rev_exp_forecast.loc['% Growth', year_lower_bound+1:current_year].mean()

    #forecast revenue for years beyond the current year and below the upper bound
    for year in range(current_year+1, year_upper_bound+1):
        rev_exp_forecast.loc['% Growth', year] = average_growth_rate
        rev_exp_forecast.loc['Revenue', year] = rev_exp_forecast.loc['Revenue', year-1] * (1 + average_growth_rate)

    #forecast expenses for years beyond the current year and below the upper bound
    

    return rev_exp_forecast
