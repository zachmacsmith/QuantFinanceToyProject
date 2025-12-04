import sys
import os
import matplotlib.pyplot as plt
import pandas as pd

print("DEBUG: main.py loaded")

# Add the current directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import fetch_data
from analysis import check_cointegration, calculate_hedge_ratio, calculate_spread, calculate_zscore
from strategy import generate_signals
from backtest import calculate_returns

from kalman import run_kalman_strategy

def run_experiment(tickers, start_date, end_date, name, use_kalman=False):
    print(f"\n--- Pairs Trading Strategy: {name} ({tickers[0]} vs {tickers[1]}) ---")
    if use_kalman:
        print("Using Kalman Filter for dynamic hedge ratio.")
    
    # 1. Fetch Data
    data = fetch_data(tickers, start_date, end_date)
    if data.empty:
        print("No data fetched. Skipping.")
        return

    series1 = data[tickers[0]]
    series2 = data[tickers[1]]
    
    # 2. Analyze (Cointegration & Spread)
    if not use_kalman:
        t_stat, p_value, crit_values = check_cointegration(series1, series2)
        print(f"Cointegration Test p-value: {p_value:.4f}")
        if p_value > 0.05:
            print("Warning: p-value > 0.05. The pair might not be cointegrated.")
        else:
            print("The pair is likely cointegrated.")
            
        hedge_ratio = calculate_hedge_ratio(series1, series2)
        print(f"Hedge Ratio: {hedge_ratio:.4f}")
        
        spread = calculate_spread(series1, series2, hedge_ratio)
    else:
        spread, hedge_ratios = run_kalman_strategy(series1, series2)
        print(f"Average Dynamic Hedge Ratio: {hedge_ratios.mean():.4f}")
    
    window = 30
    zscore = calculate_zscore(spread, window)
    
    # 3. Generate Signals
    signals = generate_signals(zscore)
    
    # 4. Backtest
    metrics = calculate_returns(data, signals)
    
    final_return = metrics['cumulative_returns'].iloc[-1]
    print(f"Final Cumulative Return: {final_return:.4f} ({(final_return-1)*100:.2f}%)")
    
    # 5. Visualize
    plt.figure(figsize=(12, 10))
    
    plt.subplot(4 if use_kalman else 3, 1, 1)
    plt.plot(data[tickers[0]], label=tickers[0])
    plt.plot(data[tickers[1]], label=tickers[1])
    plt.title(f'{name} - Asset Prices')
    plt.legend()
    
    if use_kalman:
        plt.subplot(4, 1, 2)
        plt.plot(hedge_ratios, label='Dynamic Hedge Ratio')
        plt.title(f'{name} - Kalman Hedge Ratio')
        plt.legend()
    
    plt.subplot(4 if use_kalman else 3, 1, 3 if use_kalman else 2)
    plt.plot(zscore, label='Z-Score')
    plt.axhline(2.0, color='red', linestyle='--')
    plt.axhline(-2.0, color='green', linestyle='--')
    plt.axhline(0, color='black', linestyle='-')
    plt.title(f'{name} - Spread Z-Score')
    plt.legend()
    
    plt.subplot(4 if use_kalman else 3, 1, 4 if use_kalman else 3)
    plt.plot(metrics['cumulative_returns'], label='Strategy Returns')
    plt.title(f'{name} - Cumulative Returns')
    plt.legend()
    
    plt.tight_layout()
    output_filename = f'performance_{name.replace(" ", "_")}.png'
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)
    plt.savefig(output_path)
    print(f"Performance plot saved to {output_path}")

def main():
    print("DEBUG: main() started")
    # Experiment 1: Classic (PEP vs KO)
    # run_experiment(['PEP', 'KO'], '2020-01-01', '2023-01-01', 'Classic_Consumer')
    
    # Experiment 2: Tech Giants (MSFT vs AAPL)
    # run_experiment(['MSFT', 'AAPL'], '2020-01-01', '2023-01-01', 'Tech_Giants')
    
    # Experiment 3: Commodities (GLD vs SLV)
    # run_experiment(['GLD', 'SLV'], '2020-01-01', '2023-01-01', 'Commodities')
    
    # Experiment 4: Crypto (BTC-USD vs ETH-USD)
    # run_experiment(['BTC-USD', 'ETH-USD'], '2020-01-01', '2023-01-01', 'Crypto')
    
    # Experiment 5: Crypto with Kalman Filter
    run_experiment(['BTC-USD', 'ETH-USD'], '2020-01-01', '2023-01-01', 'Crypto_Kalman', use_kalman=True)
    
    # Experiment 6: Commodities with Kalman Filter
    run_experiment(['GLD', 'SLV'], '2020-01-01', '2023-01-01', 'Commodities_Kalman', use_kalman=True)

if __name__ == "__main__":
    main()
