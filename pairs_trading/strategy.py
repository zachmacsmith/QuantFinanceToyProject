import pandas as pd
import numpy as np

def generate_signals(zscore, entry_threshold=2.0, exit_threshold=0.0):
    """
    Generates trading signals based on the z-score of the spread.
    
    Args:
        zscore (pd.Series): Z-score of the spread.
        entry_threshold (float): Z-score threshold to enter a trade.
        exit_threshold (float): Z-score threshold to exit a trade.
        
    Returns:
        pd.DataFrame: DataFrame with columns 'long_signal', 'short_signal', 'exit_signal', 'positions'.
        'positions' column: 1 for long the spread, -1 for short the spread, 0 for flat.
        Note: Long the spread means Long Asset 1 / Short Asset 2.
              Short the spread means Short Asset 1 / Long Asset 2.
    """
    signals = pd.DataFrame(index=zscore.index)
    signals['zscore'] = zscore
    signals['long_entry'] = zscore < -entry_threshold
    signals['short_entry'] = zscore > entry_threshold
    signals['long_exit'] = zscore >= -exit_threshold
    signals['short_exit'] = zscore <= exit_threshold
    
    # Initialize positions
    signals['positions'] = 0
    
    # Iterate to determine positions (state-dependent)
    position = 0 # 0: flat, 1: long spread, -1: short spread
    
    positions_list = []
    
    for i in range(len(signals)):
        row = signals.iloc[i]
        
        if position == 0:
            if row['long_entry']:
                position = 1
            elif row['short_entry']:
                position = -1
        elif position == 1:
            if row['long_exit']:
                position = 0
        elif position == -1:
            if row['short_exit']:
                position = 0
                
        positions_list.append(position)
        
    signals['positions'] = positions_list
    
    return signals
