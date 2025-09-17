import matplotlib.pyplot as plt
from fpdf import FPDF
import os

def generate_report(metrics: dict, start_date: str, end_date: str, filename: str = "Financial_Report.pdf"):
    """
    Generate a PDF report summarizing portfolio performance metrics and 
    comparison to benchmark (S&P 500).

    Parameters
    ----------
    metrics : dict
        Dictionary of performance results containing:
            - 'portfolio_history' (pd.DataFrame): Historical portfolio values with a 'Total' column.
            - 'total_current_value' (float): Latest portfolio value.
            - 'total_return_percent' (float): Total return percentage.
            - 'annualized_volatility' (float): Annualized risk (volatility).
            - 'sharpe_ratio' (float): Risk-adjusted return ratio.
            - 'value_at_risk' (float): Value at Risk estimate.
    start_date : str
        Start date of the analysis period (format: 'YYYY-MM-DD').
    end_date : str
        End date of the analysis period (format: 'YYYY-MM-DD').
    filename : str, optional
        Name of the output PDF file (default is "Financial_Report.pdf").

    Returns
    -------
    None
        A PDF report is saved to the specified filename. 
        The function also removes temporary chart files and prints a confirmation message.
    """

    portfolio_norm = metrics['portfolio_indexed_norm']
    benchmark_norm = metrics['benchmark_indexed_norm']

    # Plot portfolio vs S&P 500 (relative performance)
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(portfolio_norm.index, portfolio_norm, 
            color='midnightblue', linewidth=2, label="Portfolio")
    ax.plot(benchmark_norm.index, benchmark_norm, 
            color='darkred', linestyle="--", linewidth=2, label="S&P 500")
    ax.set_title('Portfolio vs S&P 500 (Indexed to 100)', fontsize=16)
    ax.set_ylabel('Value (Start = 100)', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.legend()
    ax.grid(True)

    chart_filename = 'performance_chart.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    plt.close(fig) 

    # Build PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 15, 'Portfolio Performance Report', 0, 1, 'C')
    pdf.ln(5)

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f'Analysis Period: {start_date} to {end_date}', 0, 1)
    pdf.ln(10)

    # Portfolio metrics
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Portfolio Metrics:', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f"   - Portfolio Value: {metrics['total_current_value']:.2f}", 0, 1)
    pdf.cell(0, 8, f"   - Portfolio Return: {metrics['total_return_percent']:.2f}%", 0, 1)
    pdf.cell(0, 8, f"   - Portfolio Volatility: {metrics['annualized_volatility']:.2f}%", 0, 1)
    pdf.cell(0, 8, f"   - Sharpe Ratio: {metrics['sharpe_ratio']:.2f}", 0, 1)
    pdf.cell(0, 8, f"   - Value at Risk: {metrics['value_at_risk']:.2f}", 0, 1)
    pdf.ln(5)

    # Benchmark metrics
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'S&P 500 Benchmark:', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f"   - Benchmark Return: {metrics['benchmark_total_return']:.2f}%", 0, 1)
    pdf.cell(0, 8, f"   - Benchmark Volatility: {metrics['benchmark_volatility']:.2f}%", 0, 1)
    pdf.cell(0, 8, f"   - Alpha (Excess Return): {metrics['alpha']:.2f}%", 0, 1)
    pdf.cell(0, 8, f"   - Beta (Market Sensitivity): {metrics['beta']:.2f}", 0, 1)
    pdf.ln(10)

    pdf.image(chart_filename, x=None, y=None, w=180)
    pdf.output(filename)
    os.remove(chart_filename)
    
    print(f"Report successfully generated: {filename}")