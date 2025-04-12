#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import sys
import logging
from datetime import datetime
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

COMMON_TICKERS = {
    "Indices": {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Dow Jones": "^DJI"
    },
    "Commodities": {
        "Gold": "GLD",  # Data from 2004
        "Silver": "SLV", # Data from 2006
    }
}

def print_usage():
    print("\nUsage: python retroAsset50WMAvsHold.py <ticker_symbol> <start_year> <end_year>")
    print("\nExample: python retroAsset50WMAvsHold.py ^GSPC 1970 1990")
    print("\nCommon ticker symbols:")
    for category, tickers in COMMON_TICKERS.items():
        print(f"\n{category}:")
        for name, symbol in tickers.items():
            print(f"  {name}: {symbol}")
    print("\nNote: Data availability varies by ticker:")
    print("  - ^GSPC (S&P 500): Data from 1927")
    print("  - ^IXIC (NASDAQ): Data from 1971")
    print("  - ^DJI (Dow Jones): Data from 1927")
    print("  - GLD (Gold ETF): Data from 2004")
    print("  - SLV (Silver ETF): Data from 2006")
    sys.exit(1)

def analyze_asset(ticker, start_year, end_year):
    start_date = f"{start_year}-01-01"
    end_date = f"{end_year}-12-31"
    
    logging.info(f"Analyzing {ticker} from {start_date} to {end_date}")
    
    # Download data
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if data.empty:
        logging.error(f"No data found for ticker {ticker} in specified date range")
        print_usage()
        
    dates = np.array(data.index)
    prices = np.array(data['Close']).flatten()
    
    logging.info(f"Data points: {len(prices)}")
    logging.info(f"First date: {dates[0]}, Last date: {dates[-1]}")
    logging.info(f"First price: {prices[0]:.2f}, Last price: {prices[-1]:.2f}")

    # Initial investment
    initial_investment = 1000

    # Calculate moving averages
    ma_200 = np.zeros(len(prices))
    ma_50w = np.zeros(len(prices))

    for i in range(len(prices)):
        if i == 0:
            ma_200[i] = prices[0]
            ma_50w[i] = prices[0]
        else:
            start_200 = max(0, i-200)
            start_50w = max(0, i-350)
            ma_200[i] = np.mean(prices[start_200:i])
            ma_50w[i] = np.mean(prices[start_50w:i])

    # Calculate daily returns
    daily_returns = np.diff(prices) / prices[:-1]
    daily_returns = np.insert(daily_returns, 0, 0)
    
    # Log return statistics
    logging.info(f"Average daily return: {np.mean(daily_returns):.4f}")
    logging.info(f"Max daily return: {np.max(daily_returns):.4f}")
    logging.info(f"Min daily return: {np.min(daily_returns):.4f}")

    # Buy and Hold strategy
    buy_hold = initial_investment * np.cumprod(1 + daily_returns)

    # 200DMA Strategy
    position_200 = prices > ma_200
    returns_200 = daily_returns * np.roll(position_200, 1)
    returns_200[0] = 0
    value_200 = initial_investment * np.cumprod(1 + returns_200)

    # Log position changes for 200DMA
    position_changes_200 = np.diff(position_200.astype(int))
    num_trades_200 = np.sum(np.abs(position_changes_200))

    # 50WMA Strategy
    position_50w = prices > ma_50w
    returns_50w = daily_returns * np.roll(position_50w, 1)
    returns_50w[0] = 0
    value_50w = initial_investment * np.cumprod(1 + returns_50w)

    # Log position changes for 50WMA
    position_changes_50w = np.diff(position_50w.astype(int))
    num_trades_50w = np.sum(np.abs(position_changes_50w))

    # Calculate and log total returns
    total_return_hold = (buy_hold[-1] / initial_investment - 1) * 100
    total_return_200 = (value_200[-1] / initial_investment - 1) * 100
    total_return_50w = (value_50w[-1] / initial_investment - 1) * 100
    
    logging.info(f"Buy & Hold final value: ${buy_hold[-1]:.2f}")
    logging.info(f"200DMA Strategy final value: ${value_200[-1]:.2f}")
    logging.info(f"50WMA Strategy final value: ${value_50w[-1]:.2f}")
    logging.info(f"Number of 200DMA trades: {num_trades_200}")
    logging.info(f"Number of 50WMA trades: {num_trades_50w}")
    logging.info(f"Total returns:")
    logging.info(f"Buy & Hold: {total_return_hold:.2f}%")
    logging.info(f"200DMA: {total_return_200:.2f}%")
    logging.info(f"50WMA: {total_return_50w:.2f}%")

    # Calculate years (fix the date calculation)
    start_date = pd.to_datetime(dates[0])
    end_date = pd.to_datetime(dates[-1])
    years = (end_date - start_date).days / 365.25
    
    # Calculate annualized returns
    ann_return_hold = (((buy_hold[-1] / initial_investment) ** (1/years)) - 1) * 100
    ann_return_200 = (((value_200[-1] / initial_investment) ** (1/years)) - 1) * 100
    ann_return_50w = (((value_50w[-1] / initial_investment) ** (1/years)) - 1) * 100
    
    logging.info(f"Annualized returns:")
    logging.info(f"Buy & Hold: {ann_return_hold:.2f}%")
    logging.info(f"200DMA: {ann_return_200:.2f}%")
    logging.info(f"50WMA: {ann_return_50w:.2f}%")

    # Plot
    plt.figure(figsize=(15, 8))
    plt.plot(dates, buy_hold, label='Buy & Hold', color='black', linewidth=5)
    plt.plot(dates, value_200, label='200DMA Strategy', color='green', linestyle='--', linewidth=5)
    plt.plot(dates, value_50w, label='50WMA Strategy', color='red', linestyle='-.', linewidth=5)
    plt.title(f'{ticker}: $1000 Investment ({start_year}-{end_year})\nBuy & Hold vs Moving Average Strategies', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    if len(sys.argv) != 4:
        print_usage()
    
    ticker = sys.argv[1]
    try:
        start_year = int(sys.argv[2])
        end_year = int(sys.argv[3])
        if start_year >= end_year:
            raise ValueError("End year must be greater than start year")
    except ValueError as e:
        logging.error(f"Invalid year format: {e}")
        print_usage()
    
    analyze_asset(ticker, start_year, end_year)

if __name__ == "__main__":
    main() 