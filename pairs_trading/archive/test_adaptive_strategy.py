import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from adaptive_strategy import run_adaptive_backtest

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
print("ADAPTIVE STRATEGY TESTING")
print("Testing intelligent strategy selection on all 9 discovered pairs")
print("="*80)

results = []

for pair in pairs_to_test:
    result = run_adaptive_backtest(
        tickers=pair['tickers'],
        start_date='2022-01-01',
        end_date='2023-01-01',
        name=pair['name']
    )
    
    if result:
        results.append({
            'name': pair['name'],
            'pair': f"{pair['tickers'][0]}/{pair['tickers'][1]}",
            'strategy': result['strategy'],
            'metrics': result['metrics']
        })

# Print summary
print(f"\n{'='*80}")
print("ADAPTIVE STRATEGY SUMMARY")
print(f"{'='*80}\n")

print(f"{'Pair':<20} {'Strategy':<10} {'Half-Life':<12} {'Hurst':<10} {'Quality':<10}")
print("-" * 80)

for r in results:
    metrics = r['metrics']
    print(f"{r['pair']:<20} {r['strategy']:<10} {metrics['half_life']:<12.1f} "
          f"{metrics['hurst_exponent']:<10.3f} {metrics['overall_score']:<10.1f}")

# Count strategy selections
static_count = sum(1 for r in results if r['strategy'] == 'static')
kalman_count = sum(1 for r in results if r['strategy'] == 'kalman')

print(f"\nStrategy Selection:")
print(f"  Static: {static_count}/9 ({static_count/9*100:.1f}%)")
print(f"  Kalman: {kalman_count}/9 ({kalman_count/9*100:.1f}%)")
