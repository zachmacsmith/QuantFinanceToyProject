import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

def calculate_half_life(spread):
    """
    Calculate the half-life of mean reversion using Ornstein-Uhlenbeck process.
    
    Args:
        spread: pd.Series of spread values
        
    Returns:
        float: Half-life in days (number of periods)
    """
    spread_lag = spread.shift(1)
    spread_diff = spread - spread_lag
    
    # Drop NaN values
    spread_lag = spread_lag.dropna()
    spread_diff = spread_diff.dropna()
    
    # Align indices
    common_index = spread_lag.index.intersection(spread_diff.index)
    spread_lag = spread_lag[common_index]
    spread_diff = spread_diff[common_index]
    
    # OLS regression: spread_diff = lambda * spread_lag + epsilon
    # lambda = -log(2) / half_life
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(spread_lag.values.reshape(-1, 1), spread_diff.values)
    
    lambda_param = model.coef_[0]
    
    # Avoid division by zero or positive lambda
    if lambda_param >= 0:
        return np.inf  # No mean reversion
    
    half_life = -np.log(2) / lambda_param
    
    return half_life

def calculate_hurst_exponent(spread, max_lag=20):
    """
    Calculate Hurst exponent using R/S analysis.
    
    H < 0.5: Mean-reverting (good for pairs trading)
    H = 0.5: Random walk
    H > 0.5: Trending
    
    Args:
        spread: pd.Series of spread values
        max_lag: Maximum lag to consider
        
    Returns:
        float: Hurst exponent
    """
    lags = range(2, max_lag)
    tau = []
    
    for lag in lags:
        # Calculate standard deviation of differences
        std = np.std(spread.diff(lag).dropna())
        tau.append(std)
    
    # Linear regression on log-log plot
    log_lags = np.log(list(lags))
    log_tau = np.log(tau)
    
    # Remove any inf or nan values
    valid_idx = np.isfinite(log_lags) & np.isfinite(log_tau)
    log_lags = log_lags[valid_idx]
    log_tau = log_tau[valid_idx]
    
    if len(log_lags) < 2:
        return 0.5  # Default to random walk
    
    poly = np.polyfit(log_lags, log_tau, 1)
    hurst = poly[0]
    
    return hurst

def calculate_correlation_stability(series1, series2, window=60):
    """
    Calculate the stability of correlation over time using rolling windows.
    
    Args:
        series1, series2: pd.Series of price data
        window: Rolling window size
        
    Returns:
        float: Standard deviation of rolling correlation (lower = more stable)
    """
    # Calculate rolling correlation
    rolling_corr = series1.rolling(window).corr(series2)
    
    # Drop NaN values
    rolling_corr = rolling_corr.dropna()
    
    if len(rolling_corr) < 2:
        return 1.0  # High variance if insufficient data
    
    # Return standard deviation of rolling correlation
    return rolling_corr.std()

def score_pair_quality(spread, series1, series2):
    """
    Calculate a comprehensive quality score for a pair.
    
    Returns dict with metrics and overall score (0-100).
    """
    # Calculate metrics
    half_life = calculate_half_life(spread)
    hurst = calculate_hurst_exponent(spread)
    corr_stability = calculate_correlation_stability(series1, series2)
    
    # Score components (0-100 each)
    
    # Half-life score: optimal is 10-40 days
    if half_life < 10:
        hl_score = 50  # Too fast, might be noise
    elif half_life <= 40:
        hl_score = 100  # Optimal range
    elif half_life <= 80:
        hl_score = 70 - (half_life - 40)  # Declining
    else:
        hl_score = max(0, 30 - (half_life - 80) / 10)  # Very slow
    
    # Hurst score: lower is better (mean-reverting)
    if hurst < 0.4:
        hurst_score = 100  # Strong mean reversion
    elif hurst < 0.5:
        hurst_score = 70  # Moderate mean reversion
    elif hurst < 0.6:
        hurst_score = 40  # Weak mean reversion
    else:
        hurst_score = 0  # Trending, bad for pairs trading
    
    # Correlation stability score: lower variance is better
    if corr_stability < 0.05:
        corr_score = 100  # Very stable
    elif corr_stability < 0.10:
        corr_score = 80  # Stable
    elif corr_stability < 0.15:
        corr_score = 50  # Moderate
    else:
        corr_score = max(0, 50 - (corr_stability - 0.15) * 200)  # Unstable
    
    # Weighted overall score
    overall_score = (
        hl_score * 0.35 +
        hurst_score * 0.35 +
        corr_score * 0.30
    )
    
    return {
        'half_life': half_life,
        'hurst_exponent': hurst,
        'correlation_stability': corr_stability,
        'half_life_score': hl_score,
        'hurst_score': hurst_score,
        'correlation_score': corr_score,
        'overall_score': overall_score
    }
