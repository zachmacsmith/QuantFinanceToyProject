# Pairs Trading Strategy: From Basics to Advanced Models

This project explores **Pairs Trading**, a market-neutral statistical arbitrage strategy. We start with a classic implementation and extend it to different markets and advanced modeling techniques.

## What is Pairs Trading?
Pairs trading involves identifying two assets that move together historically (cointegrated). When they diverge, we short the outperforming asset and buy the underperforming one, betting that the spread will revert to the mean.

## Project Structure
-   **`data_loader.py`**: Fetches historical data from Yahoo Finance.
-   **`analysis.py`**: Performs cointegration tests and calculates static hedge ratios.
-   **`kalman.py`**: Implements a Kalman Filter for dynamic hedge ratio estimation.
-   **`strategy.py`**: Generates trading signals based on Z-scores.
-   **`backtest.py`**: Simulates trading performance.
-   **`main.py`**: Runs experiments and generates plots.

## Experiments & Results

We tested the strategy across three domains: **Consumer Goods**, **Tech**, **Commodities**, and **Crypto**.

### 1. Classic Consumer (PEP vs KO)
-   **Result**: **+13.76%**
-   **Insight**: Stable pair, mean-reverting behavior.
![PEP vs KO](performance_Classic_Consumer.png)

### 2. Tech Giants (MSFT vs AAPL)
-   **Result**: **-31.14%**
-   **Insight**: While correlated, tech stocks often drift apart due to idiosyncratic news. Static hedge ratio failed.
![MSFT vs AAPL](performance_Tech_Giants.png)

### 3. Crypto (BTC vs ETH) - The Power of Kalman Filter
Crypto markets are volatile. A static hedge ratio failed miserably (**-49.37%**).
However, by applying a **Kalman Filter** to dynamically adjust the hedge ratio, we turned this into a profitable strategy.

-   **Static Model**: **-49.37%**
-   **Kalman Filter**: **+17.20%**

![Crypto Kalman](performance_Crypto_Kalman.png)

## How to Run
1.  Install dependencies:
    ```bash
    pip install pandas numpy matplotlib yfinance statsmodels
    ```
2.  Run the main script:
    ```bash
    python3 pairs_trading/main.py
    ```
