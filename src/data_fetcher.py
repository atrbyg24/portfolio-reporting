import pandas as pd
import yfinance as yf

def fetch_data(portfolio_df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch historical adjusted closing prices for a list of tickers and S&P 500 (^GSPC) as a benchmark.

    Parameters
    ----------
    portfolio_df : pd.DataFrame
        DataFrame containing a 'Ticker' column with stock ticker symbols.
    start_date : str
        Start date for fetching data (format: 'YYYY-MM-DD').
    end_date : str
        End date for fetching data (format: 'YYYY-MM-DD').

    Returns
    -------
    pd.DataFrame
        DataFrame of adjusted closing prices indexed by date, 
        with tickers as columns. Missing values are forward-filled.
    """

    tickers = portfolio_df['Ticker'].tolist()
    tickers.append("^GSPC")
    
    print(f"Fetching data for tickers: {', '.join(tickers)}...")
    
    prices = yf.download(tickers, start=start_date, end=end_date)['Close']
    
    prices.ffill(inplace=True)
    
    print("Data fetching complete.")
    return prices