import fetch_data as fd
import pandas as pd
import numpy as np
import datetime as dt


class RevenueExpenseForecast:
    def __init__(self, symbol, lower_bound, upper_bound, custom_rates_matrix=None):
        """
        :param symbol: string of stock symbol
        :param lower_bound: number of quarters below current year to pull data from
        :param upper_bound: number of quarters above current year to forecast data to
        :param custom_rates_matrix: optional custom rates matrix to use for forecasting
        """

        self.symbol = symbol
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.current_year  = dt.datetime.now().timestamp()
        self.original_financials = fd.get_raw_financials(symbol, lower_bound+1)
        self.rev_exp_forecast = None
        self.init_ref_data()
        self.init_ref_rates()
        self.init_ref_forecast()



    def init_ref_data(self, other_categories=None):
        """
        initialize revenue expense forecast dataframe
        :param other_categories: optional list of other categories (str) to include in rev_exp_forecast
        """

        #default list of categories needed for revenue and expense forecast
        category_list = ['revenue',
                         'salesCost',
                         'expensesSga',
                         'researchAndDevelopmentExpense',
                         'expensesInterest',
                         'revenueIncomeInterest',
                         'revenueOther',
                         'revenueCostOther',
                         'incomeTax',
                         'incomeNet',
                         'incomeTaxRate',
                         'date',
                         'revenueGrowthRate',
                         'revenueMargin',
                         
                         ]

        if other_categories is not None:
            category_list.extend(other_categories)

        
        # for every category not in category_list, drop that category from the original_financials
        self.rev_exp_forecast = self.original_financials.copy()
        for category in self.rev_exp_forecast.keys():
            if category not in category_list:
                self.rev_exp_forecast.pop(category)
        
        # create revenueOtherNet column
        self.rev_exp_forecast['revenueOtherNet'] = self.rev_exp_forecast['revenueOther'] - self.rev_exp_forecast['revenueCostOther']
        self.rev_exp_forecast.pop('revenueCostOther')
        self.rev_exp_forecast.pop('revenueOther')


    def init_ref_rates(self):
        """
        calculate additional rates and add to rev_exp_data
        """




    def init_ref_forecast(self):
        """
        WARNING: forecast requires rates to be calculated first (init_ref_rates)
        calculate forecasted values and add to rev_exp_forecast
        """
        #add upper bound number of quarters to rev_exp_forecast
        for i in range(1, self.upper_bound+1):
            self.rev_exp_forecast.loc[len(self.rev_exp_forecast)] = [np.nan]*len(self.rev_exp_forecast.keys())




        

    
        
        