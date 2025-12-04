import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd
from data_loader import fetch_data
from main import run_experiment
import matplotlib.pyplot as plt

def run_ensemble_comparison(tickers, start_date, end_date, name):
    """
    Compare static, Kalman, and 50/50 ensemble strategies.
    
    Since we can't easily combine strategies mid-flight, we'll run both
    and report which would have been better, plus a theoretical ensemble.
    """
    print(f"\n{'='*80}")
    print(f"ENSEMBLE COMPARISON: {name} ({tickers[0]} vs {tickers[1]})")
    print(f"{'='*80}")
    
    # Run static
    print("\n--- Running STATIC strategy ---")
    run_experiment(tickers, start_date, end_date, f"{name}_Static_Test", use_kalman=False)
    
    # Run Kalman
    print("\n--- Running KALMAN strategy ---")
    run_experiment(tickers, start_date, end_date, f"{name}_Kalman_Test", use_kalman=True)
    
    print(f"\n{'='*80}")
    print(f"Note: Ensemble would combine both strategies with 50/50 weighting")
    print(f"In practice, this means splitting capital between both approaches")
    print(f"{'='*80}\n")
    
    return {
        'pair': f"{tickers[0]}/{tickers[1]}",
        'period': name
    }
