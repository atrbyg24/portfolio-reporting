# Portfolio Performance & Reporting Tool

A Python-based tool that analyzes a stock portfolio's performance and generates a comprehensive PDF report. This project demonstrates skills in data analysis with Pandas and NumPy, API integration for data fetching, and automated report generation.

## Features
- Ingests a simple CSV file defining a stock portfolio.
- Fetches historical market data from Yahoo! Finance.
- Calculates key performance metrics:
  - Total Return
  - Annualized Volatility (Risk)
  - Sharpe Ratio (Risk-Adjusted Return)
- Generates a PDF report with metrics and a performance chart.

## Technologies Used
- Python 3.11
- Pandas
- NumPy
- yfinance
- FPDF2
- Matplotlib

## Setup and Usage
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/portfolio-analyzer.git](https://github.com/your-username/portfolio-analyzer.git)
    cd portfolio-analyzer
    ```
2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
3.  **Customize your portfolio:**
    Edit the `portfolio.csv` file to include your desired stock tickers and share counts.

4.  **Run the application:**
    ```bash
    python src/main.py
    ```
    A report named `Financial_Report.pdf` will be generated in the root directory.

## Example Output
*(Include a screenshot of your generated PDF report here!)*
![Example Report Screenshot](https://your-image-host.com/report_screenshot.png)