import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import fetch_data as fd
import revenue_expense_forecast as md


if __name__ == '__main__':
    hist_income_statement = fd.get_historical_is('AAPL')
    print(hist_income_statement)



