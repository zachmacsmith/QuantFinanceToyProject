import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from itertools import combinations
from data_loader import fetch_data
from analysis import check_cointegration, calculate_hedge_ratio

@dataclass
class PairCandidate:
    """Represents a potential trading pair with its statistical properties."""
    ticker1: str
    ticker2: str
    p_value: float
    correlation: float
    hedge_ratio: float
    
    def __repr__(self):
        return f"{self.ticker1}/{self.ticker2}: p={self.p_value:.4f}, corr={self.correlation:.4f}, hedge={self.hedge_ratio:.4f}"

def discover_pairs(tickers: List[str], 
                   start_date: str, 
                   end_date: str,
                   p_value_threshold: float = 0.05,
                   correlation_threshold: float = 0.7) -> List[PairCandidate]:
    """
    Discovers cointegrated pairs from a universe of tickers.
    
    Args:
        tickers: List of ticker symbols to screen
        start_date: Start date for historical data
        end_date: End date for historical data
        p_value_threshold: Maximum p-value for cointegration test
        correlation_threshold: Minimum correlation coefficient
        
    Returns:
        List of PairCandidate objects, sorted by p-value (best first)
    """
    print(f"\n=== Pair Discovery ===")
    print(f"Screening {len(tickers)} assets for cointegrated pairs...")
    print(f"Criteria: p-value < {p_value_threshold}, correlation > {correlation_threshold}")
    
    # Fetch data for all tickers
    print(f"\nFetching data from {start_date} to {end_date}...")
    data = fetch_data(tickers, start_date, end_date)
    
    if data.empty:
        print("No data fetched. Aborting discovery.")
        return []
    
    # Filter out tickers with insufficient data
    valid_tickers = [ticker for ticker in tickers if ticker in data.columns]
    print(f"Valid tickers with data: {len(valid_tickers)}")
    
    # Test all pairwise combinations
    total_pairs = len(list(combinations(valid_tickers, 2)))
    print(f"Testing {total_pairs} pairwise combinations...\n")
    
    candidates = []
    tested = 0
    
    for ticker1, ticker2 in combinations(valid_tickers, 2):
        tested += 1
        if tested % 20 == 0:
            print(f"Progress: {tested}/{total_pairs} pairs tested...")
        
        series1 = data[ticker1]
        series2 = data[ticker2]
        
        # Calculate correlation
        correlation = series1.corr(series2)
        
        # Skip if correlation is too low
        if correlation < correlation_threshold:
            continue
        
        # Test for cointegration
        try:
            t_stat, p_value, crit_values = check_cointegration(series1, series2)
            
            # Skip if not cointegrated
            if p_value > p_value_threshold:
                continue
            
            # Calculate hedge ratio
            hedge_ratio = calculate_hedge_ratio(series1, series2)
            
            # Add to candidates
            candidate = PairCandidate(
                ticker1=ticker1,
                ticker2=ticker2,
                p_value=p_value,
                correlation=correlation,
                hedge_ratio=hedge_ratio
            )
            candidates.append(candidate)
            
        except Exception as e:
            # Skip pairs that cause errors (e.g., insufficient data variance)
            continue
    
    # Sort by p-value (lower is better)
    candidates.sort(key=lambda x: x.p_value)
    
    print(f"\n=== Discovery Complete ===")
    print(f"Found {len(candidates)} cointegrated pairs out of {total_pairs} tested")
    
    return candidates

def print_discovery_results(candidates: List[PairCandidate], top_n: int = 10):
    """Prints a formatted table of discovery results."""
    if not candidates:
        print("No pairs found.")
        return
    
    print(f"\n=== Top {min(top_n, len(candidates))} Pairs ===")
    print(f"{'Rank':<6} {'Pair':<15} {'P-Value':<12} {'Correlation':<12} {'Hedge Ratio':<12}")
    print("-" * 65)
    
    for i, candidate in enumerate(candidates[:top_n], 1):
        pair_name = f"{candidate.ticker1}/{candidate.ticker2}"
        print(f"{i:<6} {pair_name:<15} {candidate.p_value:<12.4f} {candidate.correlation:<12.4f} {candidate.hedge_ratio:<12.4f}")
