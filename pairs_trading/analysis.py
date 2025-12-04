import statsmodels.tsa.stattools as ts
import statsmodels.api as sm
import pandas as pd
import numpy as np

def check_cointegration(series1, series2):
    """
    Checks for cointegration between two time series using the Engle-Granger test.
    
    Args:
        series1 (pd.Series): Price series of asset 1.
        series2 (pd.Series): Price series of asset 2.
        
    Returns:
        tuple: (t-statistic, p-value, critical_values)
    """
    # The null hypothesis is that there is no cointegration.
    # A low p-value (< 0.05) indicates we can reject the null hypothesis (i.e., they are cointegrated).
    result = ts.coint(series1, series2)
    t_stat = result[0]
    p_value = result[1]
    crit_values = result[2]
    
    return t_stat, p_value, crit_values

def calculate_hedge_ratio(series1, series2):
    """
    Calculates the hedge ratio using OLS regression.
    spread = series1 - hedge_ratio * series2
    """
    # Add a constant to the independent variable (series2) for the regression
    X = sm.add_constant(series2)
    model = sm.OLS(series1, X).fit()
    return model.params.iloc[1] # The slope coefficient

def calculate_spread(series1, series2, hedge_ratio):
    """
    Calculates the spread between two assets.
    """
    return series1 - hedge_ratio * series2

def calculate_zscore(spread, window):
    """
    Calculates the rolling z-score of the spread.
    """
    mean = spread.rolling(window=window).mean()
    std = spread.rolling(window=window).std()
    zscore = (spread - mean) / std
    return zscore
