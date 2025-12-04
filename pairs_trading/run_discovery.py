import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pair_discovery import discover_pairs, print_discovery_results
from main import run_experiment

# Curated universe - 50 highly liquid blue-chip stocks
ASSET_UNIVERSE = {
    'Tech': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD', 'INTC', 'CSCO', 'ORCL', 'CRM'],
    'Finance': ['JPM', 'BAC', 'GS', 'MS', 'WFC', 'C', 'BLK', 'SCHW', 'AXP', 'USB'],
    'Consumer': ['PEP', 'KO', 'MCD', 'SBUX', 'NKE', 'DIS', 'HD', 'LOW', 'TGT', 'WMT'],
    'Healthcare': ['JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'ABT', 'DHR', 'MRK', 'LLY', 'AMGN'],
    'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'OXY', 'EOG', 'PXD', 'MPC', 'VLO', 'PSX']
}

def run_period_comparison():
    """Run discovery across multiple training periods for comparison."""
    
    # Flatten asset universe
    all_tickers = []
    for tickers in ASSET_UNIVERSE.values():
        all_tickers.extend(tickers)
    
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE TRAINING PERIOD ANALYSIS")
    print(f"Asset Universe: {len(all_tickers)} stocks")
    print(f"{'='*80}")
    
    # Define training periods
    periods = [
        {'name': '2-Year', 'start': '2020-01-01', 'end': '2022-01-01'},
        {'name': '5-Year', 'start': '2017-01-01', 'end': '2022-01-01'},
        {'name': '10-Year', 'start': '2012-01-01', 'end': '2022-01-01'}
    ]
    
    # Out-of-sample test period
    test_start = '2022-01-01'
    test_end = '2023-01-01'
    
    results_summary = []
    
    for period in periods:
        print(f"\n{'='*80}")
        print(f"{period['name']} TRAINING PERIOD ({period['start']} to {period['end']})")
        print(f"{'='*80}")
        
        # Run discovery
        candidates = discover_pairs(
            tickers=all_tickers,
            start_date=period['start'],
            end_date=period['end'],
            p_value_threshold=0.05,
            correlation_threshold=0.7
        )
        
        print_discovery_results(candidates, top_n=10)
        
        # Backtest top 3 pairs
        print(f"\n{'-'*80}")
        print(f"BACKTESTING TOP 3 PAIRS (Out-of-Sample: {test_start} to {test_end})")
        print(f"{'-'*80}")
        
        backtest_results = []
        
        for i, candidate in enumerate(candidates[:3], 1):
            print(f"\n--- Pair {i}: {candidate.ticker1} / {candidate.ticker2} ---")
            
            # We'll capture the return by running the experiment
            # For now, let's just run it
            run_experiment(
                tickers=[candidate.ticker1, candidate.ticker2],
                start_date=test_start,
                end_date=test_end,
                name=f"{period['name']}_Discovered_{candidate.ticker1}_{candidate.ticker2}",
                use_kalman=False
            )
        
        # Store summary
        results_summary.append({
            'period': period['name'],
            'pairs_found': len(candidates),
            'top_pairs': candidates[:3] if len(candidates) >= 3 else candidates
        })
    
    # Print comparison summary
    print(f"\n{'='*80}")
    print(f"TRAINING PERIOD COMPARISON SUMMARY")
    print(f"{'='*80}\n")
    
    print(f"{'Period':<15} {'Pairs Found':<15} {'Top 3 Pairs'}")
    print(f"{'-'*80}")
    
    for result in results_summary:
        pairs_str = ', '.join([f"{p.ticker1}/{p.ticker2}" for p in result['top_pairs']])
        print(f"{result['period']:<15} {result['pairs_found']:<15} {pairs_str}")
    
    # Save detailed results
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'period_comparison_results.txt')
    with open(output_file, 'w') as f:
        f.write("=== TRAINING PERIOD COMPARISON ===\n")
        f.write(f"Asset Universe: {len(all_tickers)} stocks\n")
        f.write(f"Out-of-Sample Test: {test_start} to {test_end}\n\n")
        
        for result in results_summary:
            f.write(f"\n{result['period']} Training Period:\n")
            f.write(f"  Pairs Found: {result['pairs_found']}\n")
            f.write(f"  Top 3 Pairs:\n")
            for i, pair in enumerate(result['top_pairs'], 1):
                f.write(f"    {i}. {pair.ticker1}/{pair.ticker2} - p={pair.p_value:.4f}, corr={pair.correlation:.4f}\n")
    
    print(f"\nDetailed results saved to {output_file}")

if __name__ == "__main__":
    run_period_comparison()
