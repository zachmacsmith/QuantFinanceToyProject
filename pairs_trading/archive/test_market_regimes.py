import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import run_experiment
import pandas as pd

# Test the best performing pairs across different market regimes
test_pairs = [
    {'tickers': ['NKE', 'TMO'], 'name': 'NKE_TMO'},      # Best in 2022-2023 (+55%)
    {'tickers': ['INTC', 'AMGN'], 'name': 'INTC_AMGN'},  # Good in 2022-2023 (+28%)
    {'tickers': ['NVDA', 'PFE'], 'name': 'NVDA_PFE'},    # Good static (+31%)
]

# Different market regimes - CONSISTENT 1-YEAR PERIODS
test_periods = [
    {'name': 'Bull_2017', 'start': '2017-01-01', 'end': '2018-01-01', 'regime': 'Bull Market'},
    {'name': 'Crash_2019', 'start': '2019-01-01', 'end': '2020-01-01', 'regime': 'Pre-COVID'},
    {'name': 'COVID_2020', 'start': '2020-01-01', 'end': '2021-01-01', 'regime': 'COVID Crash'},
    {'name': 'Recovery_2021', 'start': '2021-01-01', 'end': '2022-01-01', 'regime': 'Recovery'},
    {'name': 'Volatile_2022', 'start': '2022-01-01', 'end': '2023-01-01', 'regime': 'Fed Hikes'},
]

print("="*80)
print("MULTI-PERIOD REGIME TESTING")
print("Testing hypothesis: 2022-2023 was uniquely bad for pairs trading")
print("="*80)

results = []

for period in test_periods:
    print(f"\n{'='*80}")
    print(f"PERIOD: {period['name']} - {period['regime']}")
    print(f"Dates: {period['start']} to {period['end']}")
    print(f"{'='*80}")
    
    for pair in test_pairs:
        print(f"\n--- Testing {pair['name']} ---")
        
        # Run static
        run_experiment(
            tickers=pair['tickers'],
            start_date=period['start'],
            end_date=period['end'],
            name=f"{period['name']}_{pair['name']}_Static",
            use_kalman=False
        )
        
        # Run Kalman
        run_experiment(
            tickers=pair['tickers'],
            start_date=period['start'],
            end_date=period['end'],
            name=f"{period['name']}_{pair['name']}_Kalman",
            use_kalman=True
        )

print(f"\n{'='*80}")
print("TESTING COMPLETE")
print("Check output/regime_testing/ for all performance plots")
print(f"{'='*80}")
