import pandas as pd
import numpy as np

def analyze_performance(prices_df: pd.DataFrame, portfolio_df: pd.DataFrame) -> dict:
    #Calculates key performance metrics for the given portfolio.
    
    portfolio_indexed = portfolio_df.set_index('Ticker')
    
    portfolio_history = prices_df * portfolio_indexed['Shares']
    
    portfolio_history['Total'] = portfolio_history.sum(axis=1)
    
    daily_returns = portfolio_history['Total'].pct_change().dropna()

    total_return = (portfolio_history['Total'].iloc[-1] / portfolio_history['Total'].iloc[0] - 1) * 100
    annualized_volatility = daily_returns.std() * np.sqrt(252) * 100
    sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)

    metrics = {
        'total_return': total_return,
        'annualized_volatility': annualized_volatility,
        'sharpe_ratio': sharpe_ratio,
        'portfolio_history': portfolio_history
    }
    
    print("Analysis complete.")
    return metrics