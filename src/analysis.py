import pandas as pd
import numpy as np

def analyze_performance(prices_df: pd.DataFrame, portfolio_df: pd.DataFrame) -> dict:
    """
    Analyze portfolio performance and compare it against the S&P 500 benchmark.

    Parameters
    ----------
    prices_df : pd.DataFrame
        DataFrame of historical adjusted closing prices for each ticker, indexed by date.
        Must include a column "^GSPC" for the S&P 500 benchmark.
    portfolio_df : pd.DataFrame
        DataFrame containing portfolio holdings with columns:
            - 'Ticker' (str): Stock ticker symbol.
            - 'Shares' (float or int): Number of shares held.

    Returns
    -------
    dict
        Dictionary containing portfolio performance metrics:
            - 'total_current_value' (float): Current portfolio value.
            - 'total_return_percent' (float): Total portfolio return over the period (%).
            - 'annualized_volatility' (float): Annualized portfolio volatility (%).
            - 'sharpe_ratio' (float): Portfolio Sharpe ratio (risk-adjusted return).
            - 'value_at_risk' (float): Value at Risk at 95% confidence level.
            - 'portfolio_history' (pd.DataFrame): Historical portfolio values, including per-ticker contributions and 'Total'.
            - 'benchmark_history' (pd.Series): Historical S&P 500 prices.
            - 'benchmark_total_return' (float): Total return of S&P 500 (%).
            - 'benchmark_volatility' (float): Annualized volatility of S&P 500 (%).
            - 'alpha' (float): Portfolio excess return over the benchmark (%).
            - 'beta' (float): Portfolio sensitivity to the benchmark (slope of regression vs S&P 500 daily returns).
            - 'portfolio_indexed_norm' (pd.Series): Portfolio value indexed to 100 at the start.
            - 'benchmark_indexed_norm' (pd.Series): Benchmark value indexed to 100 at the start.

    Notes
    -----
    - Assumes 252 trading days per year for annualized calculations.
    - Value at Risk (VaR) is calculated using historical simulation at 95% confidence.
    - Alpha is calculated as the difference between portfolio and benchmark total returns.
    - Beta is calculated via linear regression of portfolio daily returns against benchmark daily returns.
    - Normalized series are used for relative performance visualization.
    """

    
    CONFIDENCE_LEVEL = 0.95

    portfolio_indexed = portfolio_df.set_index('Ticker')
    
    portfolio_history = prices_df.drop(columns= "^GSPC") * portfolio_indexed['Shares']
    
    portfolio_history['Total'] = portfolio_history.sum(axis=1)
    total_current_value = portfolio_history['Total'].iloc[-1]
    
    daily_returns = portfolio_history['Total'].pct_change().dropna()
    total_return = (portfolio_history['Total'].iloc[-1] / portfolio_history['Total'].iloc[0] - 1) * 100
    
    std_dev = daily_returns.std()
    annualized_volatility = std_dev * np.sqrt(252) * 100
    var_percentile = daily_returns.quantile(1 - CONFIDENCE_LEVEL)
    value_at_risk = abs(total_current_value * var_percentile)
    sharpe_ratio = (daily_returns.mean() / std_dev) * np.sqrt(252) if std_dev > 0 else 0.0

    benchmark = prices_df["^GSPC"]
    benchmark_returns = benchmark.pct_change().dropna()
    benchmark_total_returns = (benchmark.iloc[-1] / benchmark.iloc[0] - 1) * 100
    benchmark_volatility = benchmark_returns.std() * np.sqrt(252) * 100

    aligned = pd.concat([daily_returns, benchmark_returns], axis=1).dropna()
    aligned.columns = ["Portfolio", "Benchmark"]

    if len(aligned) > 1:
        beta, _ = np.polyfit(aligned["Benchmark"], aligned["Portfolio"], 1)
    else:
        beta = np.nan
    
    alpha = total_return - benchmark_total_returns

    portfolio_indexed_norm = portfolio_history['Total'] / portfolio_history['Total'].iloc[0] * 100
    benchmark_indexed_norm = benchmark / benchmark.iloc[0] * 100
    
    metrics = {
        'total_current_value': total_current_value,
        'total_return_percent': total_return,
        'annualized_volatility': annualized_volatility,
        'sharpe_ratio': sharpe_ratio,
        'value_at_risk': value_at_risk,
        'portfolio_history': portfolio_history,
        'benchmark_history': benchmark,
        'benchmark_total_return': benchmark_total_returns,
        'benchmark_volatility': benchmark_volatility,
        'alpha': alpha,
        'beta': beta,
        'portfolio_indexed_norm': portfolio_indexed_norm,
        'benchmark_indexed_norm': benchmark_indexed_norm,
    }
    
    print("Analysis complete.")
    return metrics