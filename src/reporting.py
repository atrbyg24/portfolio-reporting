import matplotlib.pyplot as plt
from fpdf import FPDF
import os

def generate_report(metrics: dict, start_date: str, end_date: str, filename: str = "Financial_Report.pdf"):
    """
    Generate a PDF report summarizing portfolio performance metrics and 
    including a chart of portfolio value over time.

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

    portfolio_history = metrics['portfolio_history']
    
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(portfolio_history['Total'], color='midnightblue', linewidth=2)
    ax.set_title('Portfolio Value Over Time', fontsize=16)
    ax.set_ylabel('Portfolio Value ($)', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.grid(True)
    
    chart_filename = 'performance_chart.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    plt.close(fig) 

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    
    pdf.cell(0, 15, 'Portfolio Performance Report', 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f'Analysis Period: {start_date} to {end_date}', 0, 1)
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Key Performance Indicators:', 0, 1)
    pdf.set_font('Arial', '', 12)
    
    pdf.cell(0, 8, f"   - Total Current Value: {metrics['total_current_value']:.2f}", 0, 1)
    pdf.cell(0, 8, f"   - Total Return: {metrics['total_return_percent']:.2f}%", 0, 1)
    pdf.cell(0, 8, f"   - Annualized Volatility (Risk): {metrics['annualized_volatility']:.2f}%", 0, 1)
    pdf.cell(0, 8, f"   - Sharpe Ratio (Risk-Adjusted Return): {metrics['sharpe_ratio']:.2f}", 0, 1)
    pdf.cell(0, 8, f"   - Value at Risk: {metrics['value_at_risk']:.2f}", 0, 1)
    pdf.ln(10)
    
    pdf.image(chart_filename, x=None, y=None, w=180)
    
    pdf.output(filename)
    
    os.remove(chart_filename)
    
    print(f"Report successfully generated: {filename}")