# Archive Directory

This directory contains test scripts and experimental files that were used during development but are not part of the core project.

## Archived Test Scripts

### `debug_kalman.py`
Early debug script for testing Kalman Filter imports.

### `test_kalman_on_discoveries.py`
Script that tested Kalman Filter vs Static on all 9 discovered pairs.
**Result**: Kalman helped 4/9 pairs (44% success rate).

### `test_adaptive_strategy.py`
Script that tested the adaptive strategy selection system.
**Result**: Selected Kalman for all 9 pairs (100%) due to high correlation instability in 2022-2023.

### `test_ensemble.py`
Experimental ensemble strategy implementation (incomplete).

### `test_market_regimes.py`
Multi-period regime testing script (5 consecutive 1-year windows).
**Result**: 2022 was BEST for static (+37.97%), Kalman dominated 2017-2021.

### `ensemble_strategy.py`
Experimental ensemble strategy module (simplified version).

## Archived Analysis

### `regime_analysis.md`
Initial regime analysis with 2-year windows (incorrect comparison).
Replaced by `regime_analysis_corrected.md` with consistent 1-year windows.

## Note

These files are kept for reference but are not needed for running the core project.
The main findings from these experiments are documented in the main `README.md`.
