import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Starting debug script")
try:
    import kalman
    print("Imported kalman successfully")
except Exception as e:
    print(f"Failed to import kalman: {e}")

try:
    from kalman import run_kalman_strategy
    print("Imported run_kalman_strategy successfully")
except Exception as e:
    print(f"Failed to import run_kalman_strategy: {e}")

print("Debug script finished")
