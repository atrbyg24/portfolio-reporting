import pandas as pd
from datetime import date
from data_fetcher import fetch_data
from analysis import analyze_performance
from reporting import generate_report

def run_analysis():
    start_date = '2025-01-01'
    end_date = date.today().strftime('%Y-%m-%d')
    portfolio_df = pd.read_csv('portfolio.csv')
    prices_df = fetch_data(portfolio_df, '2024-01-01', '2025-08-18')
    metrics = analyze_performance(prices_df, portfolio_df)
    generate_report(metrics,start_date,end_date)
    print("Analysis complete. Report generated.")

if __name__ == '__main__':
    run_analysis()
