import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import fetch_data as fd
import revenue_expense_forecast as md


if __name__ == '__main__':
    rev_exp_forecast = md.get_rev_exp_forecast('AAPL')
    print(rev_exp_forecast)



