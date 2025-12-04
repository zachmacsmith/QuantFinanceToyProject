import numpy as np
import pandas as pd

class KalmanFilterReg:
    """
    Kalman Filter for online linear regression.
    Estimates the state vector [beta, alpha] where y = beta * x + alpha + noise.
    """
    def __init__(self, delta=1e-5, R=1e-3):
        # delta: process noise covariance (random walk variance)
        # R: measurement noise covariance
        
        self.n_states = 2 # Slope (beta) and Intercept (alpha)
        
        # State vector [beta, alpha]
        self.state_mean = np.zeros(self.n_states)
        
        # State covariance matrix
        self.state_cov = np.zeros((self.n_states, self.n_states))
        
        # Process noise covariance
        self.Q = delta / (1 - delta) * np.eye(self.n_states)
        
        # Measurement noise covariance
        self.R = R
        
    def update(self, x, y):
        """
        Update the state estimate with a new observation.
        x: independent variable (e.g., price of asset 2)
        y: dependent variable (e.g., price of asset 1)
        """
        # Observation matrix H = [x, 1]
        H = np.array([x, 1.0])
        
        # Prediction step (Random Walk: x_t|t-1 = x_t-1|t-1)
        # P_t|t-1 = P_t-1|t-1 + Q
        self.state_cov = self.state_cov + self.Q
        
        # Measurement residual
        y_pred = H.dot(self.state_mean)
        residual = y - y_pred
        
        # Residual covariance
        S = H.dot(self.state_cov).dot(H.T) + self.R
        
        # Kalman Gain
        K = self.state_cov.dot(H.T) / S
        
        # Update state estimate
        self.state_mean = self.state_mean + K * residual
        
        # Update state covariance
        self.state_cov = (np.eye(self.n_states) - np.outer(K, H)).dot(self.state_cov)
        
        return self.state_mean

def run_kalman_strategy(series1, series2):
    """
    Runs the Kalman Filter on the pair to get dynamic hedge ratios and spread.
    
    Returns:
        pd.Series: Spread calculated using dynamic hedge ratio.
        pd.Series: Dynamic hedge ratio (beta).
    """
    kf = KalmanFilterReg(delta=1e-5, R=1e-3)
    
    hedge_ratios = []
    intercepts = []
    spreads = []
    
    # Iterate through the data
    for t in range(len(series1)):
        x = series2.iloc[t]
        y = series1.iloc[t]
        
        state = kf.update(x, y)
        beta = state[0]
        alpha = state[1]
        
        hedge_ratios.append(beta)
        intercepts.append(alpha)
        
        # Calculate spread error: e = y - (beta * x + alpha)
        # Note: This is the prediction error (innovation) if we used the PREVIOUS state,
        # but here we use the CURRENT updated state for the spread definition usually.
        # Standard pairs trading spread: Spread = y - beta * x
        # Or Spread = y - (beta * x + alpha)
        
        spread = y - (beta * x + alpha)
        spreads.append(spread)
        
    return pd.Series(spreads, index=series1.index), pd.Series(hedge_ratios, index=series1.index)
