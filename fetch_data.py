#
#   Written by: Alex Cohen
#   API: IEX Cloud https://iexcloud.io/docs/api/
#   TODO: workaround on IEX Cloud API 4year lower limit for financials
#
#

import pandas as pd
import requests
from privtoken import IEX_CLOUD_API_TOKEN


def get_price_history(symbol, range):
    """
    :param symbol: string of stock symbol
    :param range: number of years of price history to retrieve
    :return: pandas dataframe of 1year price history of stock symbol
    """
    
    # api request from IEX cloud
    price_history_api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/chart/{range}y?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(price_history_api_url).json()

    # append historical price data from api request to pd dataframe
    df_columns = ['date', 'closing price']
    historical_prices = pd.DataFrame(columns=df_columns)
    for idx, day in enumerate(data):
        historical_prices.loc[idx] = [day['date'], day['close']]

    return historical_prices


def remove_date_intervals(df_hist_prices, interval):
    """
    :param df_hist_prices: pandas dataframe of historical prices
    :param interval: how often (in indices) to keep data
    :return: modified df_hist_prices with removed intervals
    """
    df_hist_prices = remove_date_intervals(df_hist_prices, 2)
    return df_hist_prices


def get_income_statement(symbol):
    """
    :param symbol: string of stock symbol
    :return: list of i/s dictionaries over the last 4 years sorted in descending order (2022, 2021, 2020...)
    """
    # api request from IEX cloud
    is_api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/income?period=annual&last=4&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(is_api_url).json()['income']
    return data


def get_cash_flows(symbol):
    """
    :param symbol: string of stock symbol
    :return: list of cf statement dictionaries over the last 4 years sorted in descending order (2022, 2021, 2020...)
    """
    # api request from IEX cloud
    cf_api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/cash-flow?period=annual&last=4&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(cf_api_url).json()['cashflow']
    return data



def get_balance_sheet(symbol):
    """
    :param symbol: string of stock symbol
    :return: list of b/s dictionaries over the last 4 years sorted in descending order (2022, 2021, 2020...)
    """
    # api request from IEX cloud
    bs_api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/balance-sheet?period=annual&last=4&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(bs_api_url).json()['balancesheet']
    return data


def get_raw_financials(symbol, range):
    """
    :param symbol: string of stock symbol
    :param range: number of quarters of info to retrieve
    :return list of fin data dictionaries sorted in decending order (CAUTION: arbitrarily formatted dicts)
    """
    rf_api_url = f'https://cloud.iexapis.com/v1//data/CORE/fundamentals/{symbol}/quarterly?range={range}q&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(rf_api_url).json()
    return data