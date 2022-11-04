#
#   Written by: Alex Cohen
#   API: IEX Cloud https://iexcloud.io/docs/api/
#   TODO: add variable period as parameter to financial statement functions
#
#

import pandas as pd
import requests
from privtoken import IEX_CLOUD_API_TOKEN


def get_price_history(symbol):
    """
    :param symbol: string of stock symbol
    :return: pandas dataframe of 1year price history of stock symbol
    """
    # TODO: create parameter that allows adjustment of time horizon for price history
    # api request from IEX cloud
    price_history_api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/chart/1y?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(price_history_api_url).json()

    # append historical price data from api request to pd dataframe
    df_columns = ['date', 'closing price']
    historical_prices = pd.DataFrame(columns=df_columns)
    for idx, day in enumerate(data):
        historical_prices.loc[idx] = [day['date'], day['close']]

    return historical_prices



def get_income_statement(symbol):
    """
    :param symbol: string of stock symbol
    :return: list of i/s dictionaries sorted in descending order (2022, 2021, 2020...)
    """
    # api request from IEX cloud
    is_api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/income?period=annual&last=4&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(is_api_url).json()['income']
    return data


def get_cash_flows(symbol):
    """
    :param symbol: string of stock symbol
    :return: list of cf statement dictionaries sorted in descending order (2022, 2021, 2020...)
    """
    # api request from IEX cloud
    cf_api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/cash-flow?period=annual&last=4&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(cf_api_url).json()['cashflow']
    return data


def get_balance_sheet(symbol):
    """
    :param symbol: string of stock symbol
    :return: list of b/s dictionaries sorted in descending order (2022, 2021, 2020...)
    """
    # api request from IEX cloud
    bs_api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/balance-sheet?period=annual&last=4&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(bs_api_url).json()['balancesheet']
    return data


def remove_date_intervals(df_hist_prices, interval):
    """
    :param df_hist_prices: pandas dataframe of historical prices
    :param interval: how often (in indices) to keep data
    :return: modified df_hist_prices with removed intervals
    """
    for idx, i in enumerate(df_hist_prices.iterrows()):
        if idx % interval != 0:
            df_hist_prices = df_hist_prices.drop(labels=[idx], axis=0)
    return df_hist_prices


def get_raw_financials(symbol, range):
    """
    :param symbol: string of stock symbol
    :param range: number of years of statements to retrieve
    :return:
    """
    rf_api_url = f'https://sandbox.iexapis.com/stable/time-series/reported_financials/{symbol}/10-K?range={range}y&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(rf_api_url).json()
    return data
