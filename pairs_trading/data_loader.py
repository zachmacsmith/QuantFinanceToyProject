import yfinance as yf
import pandas as pd

def fetch_data(tickers, start_date, end_date):
    """
    Fetches adjusted close prices for the given tickers.
    
    Args:
        tickers (list): List of ticker symbols (e.g., ['PEP', 'KO']).
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        
    Returns:
        pd.DataFrame: DataFrame containing adjusted close prices.
    """
    print(f"Fetching data for {tickers} from {start_date} to {end_date}...")
    # If only one ticker, yfinance returns a Series or a DataFrame with one column.
    # If multiple, it returns a DataFrame.
    # We want to ensure we have a DataFrame with columns matching tickers.
    
    data = yf.download(tickers, start=start_date, end=end_date)
    
    # Check if 'Adj Close' is in columns (multi-level index or flat)
    if 'Adj Close' in data.columns:
        data = data['Adj Close']
    elif 'Close' in data.columns:
        data = data['Close']
    else:
        # If multi-level index, it might be under 'Adj Close' or 'Close' at level 0
        # But yf.download(..., group_by='ticker') might change structure.
        # Default structure is usually Level 0: Attribute, Level 1: Ticker
        # Or Level 0: Ticker, Level 1: Attribute if group_by='ticker'
        # Let's just print columns if we fail to find it.
        pass # Will likely fail later if not handled, but let's assume standard structure
        
    if isinstance(data, pd.Series):
        data = data.to_frame()
        
    # Drop rows with missing values
    data.dropna(inplace=True)
    
    return data
