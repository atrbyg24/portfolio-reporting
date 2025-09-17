import pandas as pd
import numpy as np

def analyze_performance(prices_df: pd.DataFrame, portfolio_df: pd.DataFrame) -> dict:
    """
    Analyze portfolio performance based on historical price data and share allocations.

    Parameters
    ----------
    prices_df : pd.DataFrame
        DataFrame of adjusted closing prices for each ticker, indexed by date, with tickers as columns.
    portfolio_df : pd.DataFrame
        DataFrame containing portfolio holdings. Must include:
            - 'Ticker' (str): Stock ticker symbol.
            - 'Shares' (float or int): Number of shares held.

    Returns
    -------
    dict
        Dictionary of portfolio performance metrics:
            - 'total_current_value' (float): Current portfolio value.
            - 'total_return_percent' (float): Total return percentage over the period.
            - 'annualized_volatility' (float): Annualized risk (volatility) as a percentage.
            - 'sharpe_ratio' (float): Risk-adjusted return ratio.
            - 'value_at_risk' (float): Value at Risk at 95% confidence level.
            - 'portfolio_history' (pd.DataFrame): Portfolio value over time, including per-ticker contributions and a 'Total' column.

    Notes
    -----
    - Assumes 252 trading days per year for annualized calculations.
    - Value at Risk (VaR) is calculated using the historical simulation method at a 95% confidence level.
    """

    
    CONFIDENCE_LEVEL = 0.95

    portfolio_indexed = portfolio_df.set_index('Ticker')
    
    portfolio_history = prices_df * portfolio_indexed['Shares']
    
    portfolio_history['Total'] = portfolio_history.sum(axis=1)
    total_current_value = portfolio_history['Total'].iloc[-1]
    
    daily_returns = portfolio_history['Total'].pct_change().dropna()

    total_return = (portfolio_history['Total'].iloc[-1] / portfolio_history['Total'].iloc[0] - 1) * 100
    std_dev = daily_returns.std()
    annualized_volatility = std_dev * np.sqrt(252) * 100
    var_percentile = daily_returns.quantile(1 - CONFIDENCE_LEVEL)
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
        'value_at_risk': value_at_risk,
        'portfolio_history': portfolio_history
    }
    
    print("Analysis complete.")
    return metrics