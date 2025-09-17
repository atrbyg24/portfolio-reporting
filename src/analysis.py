import pandas as pd
import numpy as np

def analyze_performance(prices_df: pd.DataFrame, portfolio_df: pd.DataFram, confidence_level: float=0.95) -> dict:
    """
    Calculates key performance metrics for the portfolio, including
    total current value and historical Value at Risk (VaR).
    
    Args:
        prices_df (pd.DataFrame): DataFrame of historical prices for each ticker.
        portfolio_df (pd.DataFrame): DataFrame with 'Ticker' and 'Shares' columns.
        confidence_level (float): The confidence level for VaR calculation (e.g., 0.95 for 95%).

    Returns:
        dict: A dictionary containing the calculated performance metrics.
    """
    
    portfolio_indexed = portfolio_df.set_index('Ticker')
    
    portfolio_history = prices_df * portfolio_indexed['Shares']
    
    portfolio_history['Total'] = portfolio_history.sum(axis=1)
    total_current_value = portfolio_history['Total'].iloc[-1]
    
    daily_returns = portfolio_history['Total'].pct_change().dropna()

    total_return = (portfolio_history['Total'].iloc[-1] / portfolio_history['Total'].iloc[0] - 1) * 100
    std_dev = daily_returns.std()
    annualized_volatility = std_dev * np.sqrt(252) * 100
    var_percentile = daily_returns.quantile(1 - confidence_level)
    value_at_risk = abs(total_current_value * var_percentile)

    if std_dev == 0:
        sharpe_ratio = 0.0
    else:
        sharpe_ratio = (daily_returns.mean() / std_dev) * np.sqrt(252)

    metrics = {
        'total_current_value': total_current_value,
        'total_return_percent': total_return,
        'annualized_volatility': annualized_volatility,
        'sharpe_ratio': sharpe_ratio,
        f'var_{int(confidence_level * 100)}': value_at_risk,
        'portfolio_history': portfolio_history
    }
    
    print("Analysis complete.")
    return metrics