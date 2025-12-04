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
    
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True, progress=False)
    
    # Handle multi-level columns for multiple tickers
    if isinstance(data.columns, pd.MultiIndex):
        # For multiple tickers, yfinance returns MultiIndex columns
        # Structure: ('Price', 'Ticker') where Price is Close, High, Low, etc.
        if 'Close' in data.columns.get_level_values(0):
            data = data['Close']
    elif 'Close' in data.columns:
        # Single level index
        data = data[['Close']]
        
    if isinstance(data, pd.Series):
        data = data.to_frame()
    
    # Drop columns (tickers) that have too much missing data
    threshold = len(data) * 0.8  # Require at least 80% of data
    data = data.dropna(axis=1, thresh=threshold)
        
    # Drop rows with any remaining missing values
    data.dropna(inplace=True)
    
    if data.empty:
        print("Warning: Data is empty after processing!")
    
    return data
