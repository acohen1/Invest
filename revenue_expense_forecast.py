import fetch_data as fd
import pandas as pd
import numpy as np
import datetime

#TODO: make other functions modify self.rev_exp_forecast directly instead of returning a new df (for consistency); also make sure to update the docstrings
#TODO: continue to implement functionality for custom rate entries (modify forecast_df, etc.)
class RevenueExpenseForecast:
    def __init__(self, symbol, year_lower_bound, year_upper_bound, custom_rates_matrix=None):
        """
        :param symbol: stock symbol (str)
        :param year_lower_bound: lower bound of years to forecast (int)
        :param year_upper_bound: upper bound of years to forecast (int)
        :param custom_rates_matrix: pandas dataframe consisting of custom rates for each rev exp category (optional)
        """
        self.symbol = symbol
        self.current_year = datetime.datetime.now().year
        self.year_lower_bound = year_lower_bound
        self.year_upper_bound = year_upper_bound

        self.rev_exp_forecast = self.generate_df()
        self.rev_exp_forecast = self.populate_df()
        if custom_rates_matrix is None:
            self.forecast_df()
        
        

    def generate_df(self):
        """
        WARNING: current year_lower_bound is limited to 3 years before current year (IEX cloud api limitation)
        :return: empty dataframe with revenue expense formatting
        """
        year_lower_bound = self.year_lower_bound
        year_upper_bound = self.year_upper_bound
        current_year = self.current_year


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

        for year in range(year_lower_bound - current_year, year_upper_bound - current_year+1):
            df_columns.append(current_year + year)
        rev_exp_forecast = pd.DataFrame(index=df_index, columns=df_columns)

        for year in range(year_lower_bound, current_year+1):
            for expense_category in ['COGS', 'SG&A', 'R&D', 'Net Interest', 'Other income/expenses']:
                revenue = rev_exp_forecast.loc['Revenue', year]
                rev_exp_forecast.loc['% of Revenue', year] = rev_exp_forecast.loc[f'{expense_category}', year] / revenue


        return rev_exp_forecast
    

    def populate_df(self):
        """
        WARNING: current year_lower_bound is limited to 3 years before current year (IEX cloud api limitation)
        :return: populated revenue expense dataframe. parses dictionary data pulled from IEX cloud api using fetch_data methods
        """

        symbol = self.symbol
        rev_exp_forecast = self.rev_exp_forecast
        year_lower_bound = self.year_lower_bound
        year_upper_bound = self.year_upper_bound
        current_year = self.current_year
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
    

    def forecast_df(self):
        """
        WARNING: current implementation doesn't account for custom rates matrix; will be implemented in future versions
        Runs through each category in df and forecasts future values based on average historical growth rates
        """

        self.rev_exp_forecast = self.forecast_revenue()
        self.rev_exp_forecast = self.forecast_COGS()
        self.rev_exp_forecast = self.forecast_SGA()
        self.rev_exp_forecast = self.forecast_RD()
        self.rev_exp_forecast = self.forecast_net_interest()
        self.rev_exp_forecast = self.forecast_other()
        self.rev_exp_forecast = self.forecast_tax()
        self.rev_exp_forecast = self.forecast_net_income()

        return
    
    
    #using the data generated from populate_df, forecast revenue for years beyond the current year and below the upper bound
    def forecast_revenue(self, custom_growth_rate=None):
        """
        :param custom_growth_rate: pandas series consisting of custom growth rates for each year (optional)
        :return: rev_exp_forecast with forecasted revenue
        """

        rev_exp_forecast = self.rev_exp_forecast
        year_lower_bound = self.year_lower_bound
        year_upper_bound = self.year_upper_bound
        current_year = self.current_year


        # custom_growth_rate is a pandas series with the growth rate for each year; it is an optional parameter. 
        # If no custom growth rate is provided, the growth rate is calculated from the average of the last 3 years
        if custom_growth_rate is not None:
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.loc['% Growth', year] = custom_growth_rate[year]
                rev_exp_forecast.loc['Revenue', year] = round(rev_exp_forecast.loc['Revenue', year-1] * (1 + custom_growth_rate[year]))
        else:
            average_growth_rate = rev_exp_forecast.loc['% Growth', year_lower_bound+1:current_year].mean()
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.loc['% Growth', year] = average_growth_rate
                rev_exp_forecast.loc['Revenue', year] = round(rev_exp_forecast.loc['Revenue', year-1] * (1 + average_growth_rate))

        return rev_exp_forecast
    

    #using the data generated from populate_df, forecast COGS for years beyond the current year and below the upper bound
    def forecast_COGS(self, custom_COGS_rate=None):
        """
        :param custom_COGS_rate: pandas series consisting of custom COGS rates for each year (optional)
        :return: rev_exp_forecast with forecasted COGS
        """
        rev_exp_forecast = self.rev_exp_forecast
        year_lower_bound = self.year_lower_bound
        year_upper_bound = self.year_upper_bound
        current_year = self.current_year

        # custom_COGS_rate is a pandas series with the COGS rate for each year; it is an optional parameter. 
        # If no custom COGS rate is provided, the COGS rate is calculated from the average of the last 3 years

        # index variable is needed because multiple rows have the name %Revenue and need to be iterated through distincitvely
        COGS_rev_ratio_index = rev_exp_forecast.index.get_loc('COGS')+1
        if custom_COGS_rate is not None:
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[COGS_rev_ratio_index, year-year_lower_bound] = custom_COGS_rate[year]
                rev_exp_forecast.loc['COGS', year] = round(rev_exp_forecast.loc['Revenue', year] * custom_COGS_rate[year])
        else:
            average_COGS_rate = rev_exp_forecast.iloc[COGS_rev_ratio_index, 0:year_upper_bound - current_year].mean()
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[COGS_rev_ratio_index, year-year_lower_bound] = average_COGS_rate
                rev_exp_forecast.loc['COGS', year] = round(rev_exp_forecast.loc['Revenue', year] * average_COGS_rate)

        return rev_exp_forecast

    
    #using the data generated from populate_df, forecast SG&A for years beyond the current year and below the upper bound
    def forecast_SGA(self, custom_SGA_rate=None):
        """
        :param custom_SGA_rate: pandas series consisting of custom SG&A rates for each year (optional)
        :return: rev_exp_forecast with forecasted SG&A
        """
        rev_exp_forecast = self.rev_exp_forecast
        
        year_lower_bound = self.year_lower_bound
        year_upper_bound = self.year_upper_bound
        current_year = self.current_year

        # custom_SGA_rate is a pandas series with the SG&A rate for each year; it is an optional parameter. 
        # If no custom SG&A rate is provided, the SG&A rate is calculated from the average of the last 3 years

        # index variable is needed because multiple rows have the name %Revenue and need to be iterated through distincitvely
        SGA_rev_ratio_index = rev_exp_forecast.index.get_loc('SG&A')+1
        if custom_SGA_rate is not None:
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[SGA_rev_ratio_index, year-year_lower_bound] = custom_SGA_rate[year]
                rev_exp_forecast.loc['SG&A', year] = round(rev_exp_forecast.loc['Revenue', year] * custom_SGA_rate[year])
        else:
            average_SGA_rate = rev_exp_forecast.iloc[SGA_rev_ratio_index, 0:year_upper_bound - current_year].mean()
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[SGA_rev_ratio_index, year-year_lower_bound] = average_SGA_rate
                rev_exp_forecast.loc['SG&A', year] = round(rev_exp_forecast.loc['Revenue', year] * average_SGA_rate)

        return rev_exp_forecast

    
    #using the data generated from populate_df, forecast R&D for years beyond the current year and below the upper bound
    def forecast_RD(self, custom_RD_rate=None):
        """
        :param custom_RD_rate: pandas series consisting of custom R&D rates for each year (optional)
        :return: rev_exp_forecast with forecasted R&D
        """
        rev_exp_forecast = self.rev_exp_forecast
        year_lower_bound = self.year_lower_bound
        year_upper_bound = self.year_upper_bound
        current_year = self.current_year

        # custom_RD_rate is a pandas series with the R&D rate for each year; it is an optional parameter. 
        # If no custom R&D rate is provided, the R&D rate is calculated from the average of the last 3 years

        # index variable is needed because multiple rows have the name %Revenue and need to be iterated through distincitvely
        RD_rev_ratio_index = rev_exp_forecast.index.get_loc('R&D')+1
        if custom_RD_rate is not None:
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[RD_rev_ratio_index, year-year_lower_bound] = custom_RD_rate[year]
                rev_exp_forecast.loc['R&D', year] = round(rev_exp_forecast.loc['Revenue', year] * custom_RD_rate[year])
        else:
            average_RD_rate = rev_exp_forecast.iloc[RD_rev_ratio_index, 0:year_upper_bound - current_year].mean()
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[RD_rev_ratio_index, year-year_lower_bound] = average_RD_rate
                rev_exp_forecast.loc['R&D', year] = round(rev_exp_forecast.loc['Revenue', year] * average_RD_rate)

        return rev_exp_forecast
    

#using the data generated from populate_df, forecast net interest expense/income for years beyond the current year and below the upper bound
    def forecast_net_interest(self, custom_net_interest_rate=None):
        """
        :param custom_net_interest_rate: pandas series consisting of custom interest as % of revenue for each year (optional)
        :return: rev_exp_forecast with forecasted net interest
        """
        rev_exp_forecast = self.rev_exp_forecast
        year_lower_bound = self.year_lower_bound
        year_upper_bound = self.year_upper_bound
        current_year = self.current_year

        # custom_net_interest_rate is a pandas series with the net interest rate for each year; it is an optional parameter. 
        # If no custom net interest rate is provided, the net interest rate is calculated from the average of the last 3 years

        # index variable is needed because multiple rows have the name %Revenue and need to be iterated through distincitvely
        net_interest_rev_ratio_index = rev_exp_forecast.index.get_loc('Net Interest')+1
        if custom_net_interest_rate is not None:
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[net_interest_rev_ratio_index, year-year_lower_bound] = custom_net_interest_rate[year]
                rev_exp_forecast.loc['Net Interest', year] = round(rev_exp_forecast.loc['Revenue', year] * custom_net_interest_rate[year])
        else:
            average_net_interest_rate = rev_exp_forecast.iloc[net_interest_rev_ratio_index, 0:year_upper_bound - current_year].mean()
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[net_interest_rev_ratio_index, year-year_lower_bound] = average_net_interest_rate
                rev_exp_forecast.loc['Net Interest', year] = round(rev_exp_forecast.loc['Revenue', year] * average_net_interest_rate)

        return rev_exp_forecast
    

    #using the data generated from populate_df, forecast other income/expenses for years beyond the current year and below the upper bound
    def forecast_other(self, custom_other_rate=None):
        """
        :param custom_other_rate: pandas series consisting of custom other income/expenses as % of revenue for each year (optional)
        :return: rev_exp_forecast with forecasted other income/expenses
        """
        rev_exp_forecast = self.rev_exp_forecast
        year_lower_bound = self.year_lower_bound
        year_upper_bound = self.year_upper_bound
        current_year = self.current_year

        # custom_other_rate is a pandas series with the other income/expenses rate for each year; it is an optional parameter. 
        # If no custom other income/expenses rate is provided, the other income/expenses rate is calculated from the average of the last 3 years

        # index variable is needed because multiple rows have the name %Revenue and need to be iterated through distincitvely
        other_rev_ratio_index = rev_exp_forecast.index.get_loc('Other income/expenses')+1
        average_other_rate = rev_exp_forecast.iloc[other_rev_ratio_index, 0:year_upper_bound - current_year].mean()
        
        if custom_other_rate is not None:
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[other_rev_ratio_index, year-year_lower_bound] = custom_other_rate[year]
                rev_exp_forecast.loc['Other income/expenses', year] = round(rev_exp_forecast.loc['Revenue', year] * custom_other_rate[year])
        elif average_other_rate != 0:
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[other_rev_ratio_index, year-year_lower_bound] = average_other_rate
                rev_exp_forecast.loc['Other income/expenses', year] = round(rev_exp_forecast.loc['Revenue', year] * average_other_rate)
        else:
            for year in range(current_year+1, year_upper_bound+1):
                rev_exp_forecast.iloc[other_rev_ratio_index, year-year_lower_bound] = 0
                rev_exp_forecast.loc['Other income/expenses', year] = 0

        return rev_exp_forecast
    

    def forecast_tax(self, custom_tax_rate=None):
        """
        :param custom_tax_rate: pandas series consisting of custom income tax % for each year
        :return: rev_exp_forecast with forecasted income tax expense
        """
        rev_exp_forecast = self.rev_exp_forecast
        year_lower_bound = self.year_lower_bound
        year_upper_bound = self.year_upper_bound
        current_year = self.current_year
        
        if custom_tax_rate is None:
            #using last 3 years of data to calculate average tax rate
            average_tax_rate = rev_exp_forecast.iloc[rev_exp_forecast.index.get_loc('Tax Expense')+1, 0:year_upper_bound - current_year].mean()
            for year in range(current_year+1, year_upper_bound+1):
                #calculate yearly EBT to be used for the averaged tax expense
                EBT = self.forecast_EBT(year)
                tax_expense = round(EBT * average_tax_rate)           
                rev_exp_forecast.loc['Tax Rate', year] = average_tax_rate
                rev_exp_forecast.loc['Tax Expense', year] = tax_expense
        else:
            for year in range(current_year+1, year_upper_bound+1):
                #calculate yearly EBT to be used for the averaged tax expense
                EBT = self.forecast_EBT(rev_exp_forecast, year)
                rev_exp_forecast.loc['Tax Rate', year] = custom_tax_rate[year]
                rev_exp_forecast.loc['Tax Expense', year] = round(EBT * custom_tax_rate[year])
        
        return rev_exp_forecast


    def forecast_EBT(self, year):
        """
        :param year: year to forecast EBT for
        :return: EBT for given rev_exp_forecast and year
        """
        rev_exp_forecast = self.rev_exp_forecast
        revenue = rev_exp_forecast.loc['Revenue', year]
        COGS = rev_exp_forecast.loc['COGS', year]
        SGA = rev_exp_forecast.loc['SG&A', year]
        RD = rev_exp_forecast.loc['R&D', year]
        net_interest = rev_exp_forecast.loc['Net Interest', year]
        other = rev_exp_forecast.loc['Other income/expenses', year]
        EBT = revenue - COGS - SGA - RD - net_interest - other
        return EBT


    def forecast_net_income(self):
        """
        :param rev_exp_forecast: dataframe with revenue and expense categories populated
        :return: net income for given rev_exp_forecast
        """
        rev_exp_forecast = self.rev_exp_forecast
        year_lower_bound = rev_exp_forecast.columns[0]
        year_upper_bound = rev_exp_forecast.columns[-1]
        current_year = datetime.date.today().year

        #calculate net income using EBIT and tax rev
        for year in range(current_year+1, year_upper_bound+1):
            EBT = self.forecast_EBT(year)
            tax_expense = rev_exp_forecast.loc['Tax Expense', year]
            net_profit = EBT - tax_expense
            rev_exp_forecast.loc['Net Profit', year] = net_profit

        #calculate % margin using revenue and net income
        for year in range(current_year+1, year_upper_bound+1):
            revenue = rev_exp_forecast.loc['Revenue', year]
            net_profit = rev_exp_forecast.loc['Net Profit', year]
            rev_exp_forecast.loc['% Margin', year] = net_profit / revenue
        
        return rev_exp_forecast