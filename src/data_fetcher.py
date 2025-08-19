# src/data_fetcher.py

import pandas as pd
import yfinance as yf

def fetch_data(portfolio_df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    #Fetches historical adjusted close prices for tickers in the portfolio.

    tickers = portfolio_df['Ticker'].tolist()
    
    print(f"Fetching data for tickers: {', '.join(tickers)}...")
    
    prices = yf.download(tickers, start=start_date, end=end_date)['Close']
    
    prices.ffill(inplace=True)
    
    print("Data fetching complete.")
    return prices