import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from data_loader import fetch_data
from analysis import calculate_hedge_ratio, calculate_spread
from advanced_metrics import score_pair_quality

def select_strategy(series1, series2, verbose=True):
    """
    Intelligently select between static and Kalman Filter strategy.
    
    Decision logic:
    - If regime unstable (long half-life OR high correlation variance): Use Kalman
    - If strong mean-reversion (low Hurst): Use Static
    - Otherwise: Use Static as default
    
    Args:
        series1, series2: Price series for the pair
        verbose: Print decision reasoning
        
    Returns:
        str: 'static' or 'kalman'
    """
    # Calculate static hedge ratio and spread
    hedge_ratio = calculate_hedge_ratio(series1, series2)
    spread = calculate_spread(series1, series2, hedge_ratio)
    
    # Get quality metrics
    metrics = score_pair_quality(spread, series1, series2)
    
    half_life = metrics['half_life']
    hurst = metrics['hurst_exponent']
    corr_stability = metrics['correlation_stability']
    
    # Decision logic
    decision = 'static'  # Default
    reason = []
    
    # Check for regime instability (Kalman helps)
    if half_life > 60:
        decision = 'kalman'
        reason.append(f"Long half-life ({half_life:.1f} days) indicates slow mean reversion")
    
    if corr_stability > 0.15:
        decision = 'kalman'
        reason.append(f"High correlation variance ({corr_stability:.3f}) indicates regime instability")
    
    # Check for strong mean reversion (Static works)
    if hurst < 0.4 and decision == 'static':
        reason.append(f"Strong mean reversion (Hurst={hurst:.3f}) favors static hedge ratio")
    
    # If no strong signals, use overall score
    if not reason:
        if metrics['overall_score'] > 70:
            reason.append(f"High quality score ({metrics['overall_score']:.1f}) suggests stable relationship")
        else:
            decision = 'kalman'
            reason.append(f"Low quality score ({metrics['overall_score']:.1f}) suggests trying adaptive approach")
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"ADAPTIVE STRATEGY SELECTION")
        print(f"{'='*70}")
        print(f"Metrics:")
        print(f"  Half-Life: {half_life:.1f} days")
        print(f"  Hurst Exponent: {hurst:.3f}")
        print(f"  Correlation Stability: {corr_stability:.3f}")
        print(f"  Overall Quality Score: {metrics['overall_score']:.1f}/100")
        print(f"\nDecision: {decision.upper()}")
        print(f"Reasoning:")
        for r in reason:
            print(f"  - {r}")
        print(f"{'='*70}\n")
    
    return decision, metrics

def run_adaptive_backtest(tickers, start_date, end_date, name):
    """
    Run backtest with adaptive strategy selection.
    
    Args:
        tickers: List of two ticker symbols
        start_date, end_date: Date range
        name: Experiment name
        
    Returns:
        dict: Results including strategy used and performance
    """
    from main import run_experiment
    
    print(f"\n{'='*80}")
    print(f"ADAPTIVE BACKTEST: {name} ({tickers[0]} / {tickers[1]})")
    print(f"{'='*80}")
    
    # Fetch data
    data = fetch_data(tickers, start_date, end_date)
    
    if data.empty or len(data.columns) < 2:
        print("Insufficient data for adaptive selection")
        return None
    
    series1 = data[tickers[0]]
    series2 = data[tickers[1]]
    
    # Select strategy
    strategy, metrics = select_strategy(series1, series2, verbose=True)
    
    # Run backtest with selected strategy
    use_kalman = (strategy == 'kalman')
    
    print(f"\nRunning backtest with {strategy.upper()} strategy...")
    run_experiment(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        name=f"{name}_Adaptive_{strategy.capitalize()}",
        use_kalman=use_kalman
    )
    
    return {
        'strategy': strategy,
        'metrics': metrics
    }
