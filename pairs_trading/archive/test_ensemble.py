import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ensemble_strategy import run_ensemble_strategy
import pandas as pd

# Test pairs (best and worst performers)
test_pairs = [
    {'tickers': ['NVDA', 'PFE'], 'name': 'NVDA_PFE'},  # Best static (+31%)
    {'tickers': ['NKE', 'TMO'], 'name': 'NKE_TMO'},    # Best overall (+55%)
    {'tickers': ['INTC', 'AMGN'], 'name': 'INTC_AMGN'}, # Good static (+28%)
]

# Test periods (different market regimes)
test_periods = [
    {'name': 'Bull_2018-2019', 'start': '2018-01-01', 'end': '2019-12-31'},
    {'name': 'COVID_2020-2021', 'start': '2020-01-01', 'end': '2021-12-31'},
    {'name': 'Volatile_2022-2023', 'start': '2022-01-01', 'end': '2023-12-31'},
]

print("="*80)
print("ENSEMBLE STRATEGY TESTING")
print("Testing weighted combination across multiple market regimes")
print("="*80)

all_results = []

for period in test_periods:
    print(f"\n{'='*80}")
    print(f"PERIOD: {period['name']} ({period['start']} to {period['end']})")
    print(f"{'='*80}")
    
    period_results = []
    
    for pair in test_pairs:
        result = run_ensemble_strategy(
            tickers=pair['tickers'],
            start_date=period['start'],
            end_date=period['end'],
            name=f"{period['name']}_{pair['name']}",
            static_weight=0.5  # 50/50 ensemble
        )
        
        if result:
            result['pair'] = f"{pair['tickers'][0]}/{pair['tickers'][1]}"
            result['period'] = period['name']
            period_results.append(result)
            all_results.append(result)
    
    # Period summary
    if period_results:
        avg_static = sum(r['static_return'] for r in period_results) / len(period_results)
        avg_kalman = sum(r['kalman_return'] for r in period_results) / len(period_results)
        avg_ensemble = sum(r['ensemble_return'] for r in period_results) / len(period_results)
        
        print(f"\n{period['name']} Summary:")
        print(f"  Avg Static:   {(avg_static-1)*100:>6.2f}%")
        print(f"  Avg Kalman:   {(avg_kalman-1)*100:>6.2f}%")
        print(f"  Avg Ensemble: {(avg_ensemble-1)*100:>6.2f}%")
        print(f"  Improvement:  {(avg_ensemble-max(avg_static, avg_kalman))*100:>6.2f}%")

# Overall summary
print(f"\n{'='*80}")
print("OVERALL SUMMARY (All Periods)")
print(f"{'='*80}\n")

df = pd.DataFrame(all_results)

print(f"{'Period':<20} {'Pair':<15} {'Static':<10} {'Kalman':<10} {'Ensemble':<10} {'Best':<10}")
print("-" * 85)

for _, row in df.iterrows():
    best_single = max(row['static_return'], row['kalman_return'])
    best_name = 'Static' if row['static_return'] > row['kalman_return'] else 'Kalman'
    
    print(f"{row['period']:<20} {row['pair']:<15} "
          f"{(row['static_return']-1)*100:>6.2f}%   "
          f"{(row['kalman_return']-1)*100:>6.2f}%   "
          f"{(row['ensemble_return']-1)*100:>6.2f}%   "
          f"{best_name:<10}")

# Calculate win rates
ensemble_beats_static = sum(1 for r in all_results if r['ensemble_return'] > r['static_return'])
ensemble_beats_kalman = sum(1 for r in all_results if r['ensemble_return'] > r['kalman_return'])
ensemble_beats_both = sum(1 for r in all_results if r['ensemble_return'] > max(r['static_return'], r['kalman_return']))

total = len(all_results)

print(f"\nEnsemble Win Rates:")
print(f"  vs Static: {ensemble_beats_static}/{total} ({ensemble_beats_static/total*100:.1f}%)")
print(f"  vs Kalman: {ensemble_beats_kalman}/{total} ({ensemble_beats_kalman/total*100:.1f}%)")
print(f"  vs Best Single: {ensemble_beats_both}/{total} ({ensemble_beats_both/total*100:.1f}%)")

# Average improvements
avg_improvement_vs_static = sum(r['improvement_vs_static'] for r in all_results) / total
avg_improvement_vs_kalman = sum(r['improvement_vs_kalman'] for r in all_results) / total

print(f"\nAverage Improvements:")
print(f"  vs Static: {avg_improvement_vs_static*100:>6.2f}%")
print(f"  vs Kalman: {avg_improvement_vs_kalman*100:>6.2f}%")
