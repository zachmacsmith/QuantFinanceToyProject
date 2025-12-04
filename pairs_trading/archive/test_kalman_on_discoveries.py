import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import run_experiment

# Top pairs from each training period
pairs_to_test = [
    # 2-Year discoveries
    {'tickers': ['NVDA', 'PEP'], 'name': '2Y_NVDA_PEP'},
    {'tickers': ['GOOGL', 'ORCL'], 'name': '2Y_GOOGL_ORCL'},
    {'tickers': ['NVDA', 'PFE'], 'name': '2Y_NVDA_PFE'},
    
    # 5-Year discoveries
    {'tickers': ['AMD', 'TMO'], 'name': '5Y_AMD_TMO'},
    {'tickers': ['META', 'TGT'], 'name': '5Y_META_TGT'},
    {'tickers': ['NKE', 'TMO'], 'name': '5Y_NKE_TMO'},
    
    # 10-Year discoveries
    {'tickers': ['LOW', 'LLY'], 'name': '10Y_LOW_LLY'},
    {'tickers': ['INTC', 'AMGN'], 'name': '10Y_INTC_AMGN'},
    {'tickers': ['HD', 'UNH'], 'name': '10Y_HD_UNH'},
]

print("="*80)
print("KALMAN FILTER COMPARISON: Static vs Dynamic Hedge Ratios")
print("="*80)

for pair in pairs_to_test:
    print(f"\n{'='*80}")
    print(f"Testing: {pair['name']} ({pair['tickers'][0]} / {pair['tickers'][1]})")
    print(f"{'='*80}")
    
    # Static hedge ratio
    print(f"\n--- STATIC Hedge Ratio ---")
    run_experiment(
        tickers=pair['tickers'],
        start_date='2022-01-01',
        end_date='2023-01-01',
        name=f"{pair['name']}_Static",
        use_kalman=False
    )
    
    # Dynamic hedge ratio (Kalman Filter)
    print(f"\n--- KALMAN FILTER (Dynamic Hedge Ratio) ---")
    run_experiment(
        tickers=pair['tickers'],
        start_date='2022-01-01',
        end_date='2023-01-01',
        name=f"{pair['name']}_Kalman",
        use_kalman=True
    )

print(f"\n{'='*80}")
print("COMPARISON COMPLETE")
print(f"{'='*80}")
