import pandas as pd
import numpy as np

def calculate_returns(data, signals):
    """
    Calculates the returns of the strategy.
    
    Args:
        data (pd.DataFrame): DataFrame containing adjusted close prices of the two assets.
                             Columns should be [ticker1, ticker2].
        signals (pd.DataFrame): DataFrame containing 'positions' column.
        
    Returns:
        pd.DataFrame: DataFrame with 'daily_returns' and 'cumulative_returns'.
    """
    # Calculate daily returns of the individual assets
    asset_returns = data.pct_change()
    
    # We need to approximate the return of the spread position.
    # Long Spread = Long Asset 1 + Short Asset 2
    # Short Spread = Short Asset 1 + Long Asset 2
    
    # For simplicity in this basic implementation, we will assume equal dollar allocation 
    # to the spread when the position is on. 
    # A more precise way would be to use the hedge ratio to weight the returns.
    # Let's use the hedge ratio implicitly by trading the spread itself? 
    # No, we trade the assets.
    
    # Let's refine:
    # Position = 1 (Long Spread) -> +1 * Return_Asset1 - 1 * Return_Asset2 (simplified)
    # Actually, it should be weighted by the hedge ratio used to construct the spread.
    # Spread = Asset1 - HedgeRatio * Asset2
    # If we buy 1 unit of Asset 1, we sell HedgeRatio units of Asset 2.
    
    # However, 'data' here might not have the hedge ratio. 
    # Let's assume for this "easy" project that we just take the difference of returns 
    # as a proxy for the spread return, or better, let's pass the hedge ratio or recalculate it?
    # To keep it simple and self-contained, let's just use the position to multiply the 
    # difference in returns between the two assets.
    
    # Better approach for PnL:
    # PnL = Position * (Change in Asset1 - HedgeRatio * Change in Asset2)
    # But we want % returns.
    
    # Let's stick to a simpler approximation often used in basic pairs trading tutorials:
    # Strategy Return = Position(t-1) * (Asset1_Return - Asset2_Return)
    # This assumes a hedge ratio of 1.0 for the PnL calculation which is a simplification.
    
    # Let's try to do it slightly better. We will assume we invest capital into the pair.
    # Returns = Position * (Asset1_Ret - Asset2_Ret) is roughly correct if prices are similar.
    
    # Let's use the actual price changes.
    # Daily PnL per unit = Position * ( (Price1_t - Price1_t-1) - HedgeRatio * (Price2_t - Price2_t-1) )
    # This requires the Hedge Ratio.
    
    # Since I didn't pass hedge ratio to this function, I will modify the design slightly 
    # to accept it or just calculate returns based on the spread time series if provided?
    # No, let's just take the simple approach: 
    # Strategy Return = Position.shift(1) * (Asset1_PctChange - Asset2_PctChange)
    # This is a "Dollar Neutral" assumption where we go long $1 of A and short $1 of B (approx).
    
    strategy_returns = signals['positions'].shift(1) * (asset_returns.iloc[:, 0] - asset_returns.iloc[:, 1])
    
    metrics = pd.DataFrame(index=strategy_returns.index)
    metrics['daily_returns'] = strategy_returns
    metrics['cumulative_returns'] = (1 + metrics['daily_returns']).cumprod()
    
    return metrics
