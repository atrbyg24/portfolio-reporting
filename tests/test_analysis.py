import pytest
import pandas as pd
import numpy as np
from src.analysis import analyze_performance

@pytest.fixture
def sample_data():
    # Provides a sample portfolio and price history for testing.
    portfolio_df = pd.DataFrame({
        'Ticker': ['STOCKA', 'STOCKB'],
        'Shares': [10, 5]
    })
    
    price_data = {
        'STOCKA': [100.0, 102.0, 101.0, 105.0],
        'STOCKB': [200.0, 200.0, 204.0, 208.0]
    }
    dates = pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'])
    prices_df = pd.DataFrame(price_data, index=dates)
    
    return {'portfolio': portfolio_df, 'prices': prices_df}

def test_analyze_performance_normal_case(sample_data):
    # Tests the main analysis function with a standard multi-stock portfolio.

    portfolio = sample_data['portfolio']
    prices = sample_data['prices']
    
    results = analyze_performance(prices, portfolio)
    
    assert isinstance(results, dict)
    assert 'total_return' in results
    assert 'annualized_volatility' in results
    assert 'sharpe_ratio' in results
    assert isinstance(results['total_return'], float)
    assert results['annualized_volatility'] > 0

def test_analyze_performance_single_stock():
    # Tests the analysis function with a portfolio containing only one stock.

    portfolio_df = pd.DataFrame({'Ticker': ['STOCKA'], 'Shares': [10]})
    price_data = {'STOCKA': [100.0, 102.0, 101.0, 105.0]}
    dates = pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'])
    prices_df = pd.DataFrame(price_data, index=dates)
    
    results = analyze_performance(prices_df, portfolio_df)
    
    assert isinstance(results, dict)
    assert 'total_return' in results
    assert np.isclose(results['total_return'], 5.0)

def test_analyze_performance_flat_prices(sample_data):
    # Tests the analysis with flat prices, expecting zero volatility.

    portfolio = sample_data['portfolio']
    prices = sample_data['prices'].copy()
    prices['STOCKA'] = 100.0
    prices['STOCKB'] = 200.0
    
    results = analyze_performance(prices, portfolio)
    
    assert np.isclose(results['total_return'], 0.0)
    assert np.isclose(results['annualized_volatility'], 0.0)
    assert np.isnan(results['sharpe_ratio']) or np.isclose(results['sharpe_ratio'], 0.0)

