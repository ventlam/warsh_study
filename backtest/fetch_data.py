"""
Fetch historical data for Warsh framework backtest (2021-2024)
"""

import pandas as pd
import yfinance as yf
from datetime import datetime
import requests

def fetch_fred_data(series_id, start_date, end_date):
    """Fetch data from FRED API"""
    # For now, use simplified approach - will use actual FRED API if available
    # Fallback: manually entered key datapoints
    return None

def fetch_market_data(ticker, start_date, end_date):
    """Fetch market data from Yahoo Finance"""
    data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
    if data.empty:
        return None
    # Handle MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        return data['Adj Close'][ticker] if 'Adj Close' in data.columns.levels[0] else data['Close'][ticker]
    else:
        return data['Adj Close'] if 'Adj Close' in data.columns else data['Close']

def main():
    start_date = "2021-01-01"
    end_date = "2024-12-31"

    print("Fetching market data...")

    # Market data (daily)
    tickers = ['SPY', 'TLT', 'IEF', 'HYG', 'GLD']  # Skip DXY for now (problematic ticker)
    market_data = {}

    for ticker in tickers:
        try:
            print(f"  Downloading {ticker}...")
            data = fetch_market_data(ticker, start_date, end_date)
            if data is not None and not data.empty:
                market_data[ticker] = data
                print(f"    ✓ Got {len(data)} data points")
            else:
                print(f"    ✗ No data returned")
        except Exception as e:
            print(f"  Error fetching {ticker}: {e}")

    # Convert to monthly (end of month prices)
    monthly_data = pd.DataFrame()
    for ticker, data in market_data.items():
        monthly = data.resample('ME').last()
        monthly_data[ticker] = monthly

    # Save to CSV
    if not monthly_data.empty:
        monthly_data.to_csv('backtest/market_data_monthly.csv')
        print(f"\n✓ Market data saved: {len(monthly_data)} months")
        print(f"  Date range: {monthly_data.index[0]} to {monthly_data.index[-1]}")
    else:
        print("\n✗ No market data to save")

    # CPI data (manually entered for now - would use FRED API in production)
    cpi_data = {
        '2021-01': 1.4, '2021-02': 1.7, '2021-03': 2.6, '2021-04': 4.2,
        '2021-05': 5.0, '2021-06': 5.4, '2021-07': 5.4, '2021-08': 5.3,
        '2021-09': 5.4, '2021-10': 6.2, '2021-11': 6.8, '2021-12': 7.0,
        '2022-01': 7.5, '2022-02': 7.9, '2022-03': 8.5, '2022-04': 8.3,
        '2022-05': 8.6, '2022-06': 9.1, '2022-07': 8.5, '2022-08': 8.3,
        '2022-09': 8.2, '2022-10': 7.7, '2022-11': 7.1, '2022-12': 6.5,
        '2023-01': 6.4, '2023-02': 6.0, '2023-03': 5.0, '2023-04': 4.9,
        '2023-05': 4.0, '2023-06': 3.0, '2023-07': 3.2, '2023-08': 3.7,
        '2023-09': 3.7, '2023-10': 3.2, '2023-11': 3.1, '2023-12': 3.4,
        '2024-01': 3.1, '2024-02': 3.2, '2024-03': 3.5, '2024-04': 3.4,
        '2024-05': 3.3, '2024-06': 3.0, '2024-07': 2.9, '2024-08': 2.5,
        '2024-09': 2.4, '2024-10': 2.6, '2024-11': 2.7, '2024-12': 2.9,
    }

    cpi_df = pd.DataFrame(list(cpi_data.items()), columns=['Date', 'CPI_YoY'])
    cpi_df['Date'] = pd.to_datetime(cpi_df['Date'])
    cpi_df.set_index('Date', inplace=True)
    cpi_df.to_csv('backtest/cpi_data.csv')
    print(f"\n✓ CPI data saved: {len(cpi_df)} months")

    # Unemployment data (simplified)
    unemp_data = {
        '2021-01': 6.3, '2021-02': 6.2, '2021-03': 6.0, '2021-04': 6.1,
        '2021-05': 5.8, '2021-06': 5.9, '2021-07': 5.4, '2021-08': 5.2,
        '2021-09': 4.8, '2021-10': 4.6, '2021-11': 4.2, '2021-12': 3.9,
        '2022-01': 4.0, '2022-02': 3.8, '2022-03': 3.6, '2022-04': 3.6,
        '2022-05': 3.6, '2022-06': 3.6, '2022-07': 3.5, '2022-08': 3.7,
        '2022-09': 3.5, '2022-10': 3.7, '2022-11': 3.7, '2022-12': 3.5,
        '2023-01': 3.4, '2023-02': 3.6, '2023-03': 3.5, '2023-04': 3.4,
        '2023-05': 3.7, '2023-06': 3.6, '2023-07': 3.5, '2023-08': 3.8,
        '2023-09': 3.8, '2023-10': 3.9, '2023-11': 3.7, '2023-12': 3.7,
        '2024-01': 3.7, '2024-02': 3.9, '2024-03': 3.8, '2024-04': 3.9,
        '2024-05': 4.0, '2024-06': 4.1, '2024-07': 4.3, '2024-08': 4.2,
        '2024-09': 4.1, '2024-10': 4.1, '2024-11': 4.2, '2024-12': 4.0,
    }

    unemp_df = pd.DataFrame(list(unemp_data.items()), columns=['Date', 'Unemployment'])
    unemp_df['Date'] = pd.to_datetime(unemp_df['Date'])
    unemp_df.set_index('Date', inplace=True)
    unemp_df.to_csv('backtest/unemployment_data.csv')
    print(f"\n✓ Unemployment data saved: {len(unemp_df)} months")

    print("\n" + "="*60)
    print("Data collection complete!")
    print("="*60)

if __name__ == "__main__":
    main()
