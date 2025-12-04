import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analysis import calculate_zscore
from strategy import generate_signals

class TestPairsTrading(unittest.TestCase):
    
    def test_zscore_calculation(self):
        # Create a simple series: 1, 2, 3, 4, 5
        data = pd.Series([1, 2, 3, 4, 5])
        # Window 3
        # i=2: [1, 2, 3] -> mean=2, std=1 -> z=(3-2)/1 = 1.0
        # i=3: [2, 3, 4] -> mean=3, std=1 -> z=(4-3)/1 = 1.0
        # i=4: [3, 4, 5] -> mean=4, std=1 -> z=(5-4)/1 = 1.0
        zscore = calculate_zscore(data, window=3)
        
        self.assertTrue(np.isnan(zscore.iloc[0]))
        self.assertTrue(np.isnan(zscore.iloc[1]))
        self.assertAlmostEqual(zscore.iloc[2], 1.0)
        
    def test_signal_generation(self):
        # Create synthetic z-score series
        # 0, 3 (long entry), 1 (hold), -1 (exit), -3 (short entry), -1 (hold), 1 (exit)
        # Note: My strategy logic:
        # Long Entry < -2.0
        # Long Exit >= 0.0
        # Short Entry > 2.0
        # Short Exit <= 0.0
        
        zscores = [0.0, 2.5, 1.0, -0.1, -2.5, -1.0, 0.1]
        zscore_series = pd.Series(zscores)
        
        signals = generate_signals(zscore_series, entry_threshold=2.0, exit_threshold=0.0)
        positions = signals['positions'].tolist()
        
        # Expected behavior:
        # 0: 0.0 -> Flat (0)
        # 1: 2.5 -> Short Entry -> Short (-1)
        # 2: 1.0 -> Hold Short -> Short (-1)
        # 3: -0.1 -> Short Exit (<=0) -> Flat (0)
        # 4: -2.5 -> Long Entry -> Long (1)
        # 5: -1.0 -> Hold Long -> Long (1)
        # 6: 0.1 -> Long Exit (>=0) -> Flat (0)
        
        expected_positions = [0, -1, -1, 0, 1, 1, 0]
        self.assertEqual(positions, expected_positions)

if __name__ == '__main__':
    unittest.main()
