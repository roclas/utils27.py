#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

COMMON_TICKERS = {
    "Indices": {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Dow Jones": "^DJI"
    },
    "Crypto": {
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD"
    },
    "Commodities": {
        "Gold": "GLD",
        "Silver": "SLV",
        "Copper": "CPER",
        "Oil": "USO"
    }
}

def print_usage():
    print("\nUsage: python asset50WMAvsHold.py <ticker_symbol>")
    print("\nCommon ticker symbols:")
    for category, tickers in COMMON_TICKERS.items():
        print(f"\n{category}:")
        for name, symbol in tickers.items():
            print(f"  {name}: {symbol}")
    print("\nExample: python asset50WMAvsHold.py BTC-USD")
    sys.exit(1)

def analyze_asset(ticker):
    # Download 10 years of data
    logging.info(f"Downloading data for {ticker}")
    data = yf.download(ticker, start="2014-04-01", end="2024-04-01", progress=False)
    if data.empty:
        logging.error(f"No data found for ticker {ticker}")
        print_usage()
        
    dates = np.array(data.index)
    prices = np.array(data['Close']).flatten()
    
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

    # Log some MA values for verification
    logging.info(f"Last 200DMA: {ma_200[-1]:.2f}, Last price: {prices[-1]:.2f}")
    logging.info(f"Last 50WMA: {ma_50w[-1]:.2f}")

    # Calculate daily returns
    daily_returns = np.diff(prices) / prices[:-1]
    daily_returns = np.insert(daily_returns, 0, 0)
    
    # Log some return statistics
    logging.info(f"Average daily return: {np.mean(daily_returns):.4f}")
    logging.info(f"Max daily return: {np.max(daily_returns):.4f}")
    logging.info(f"Min daily return: {np.min(daily_returns):.4f}")

    # Buy and Hold strategy
    buy_hold = initial_investment * np.cumprod(1 + daily_returns)
    logging.info(f"Buy & Hold final value: ${buy_hold[-1]:.2f}")

    # 200DMA Strategy
    position_200 = prices > ma_200
    returns_200 = daily_returns * np.roll(position_200, 1)
    returns_200[0] = 0
    value_200 = initial_investment * np.cumprod(1 + returns_200)
    logging.info(f"200DMA Strategy final value: ${value_200[-1]:.2f}")

    # Log position changes for 200DMA
    position_changes_200 = np.diff(position_200.astype(int))
    num_trades_200 = np.sum(np.abs(position_changes_200))
    logging.info(f"Number of 200DMA trades: {num_trades_200}")

    # 50WMA Strategy
    position_50w = prices > ma_50w
    returns_50w = daily_returns * np.roll(position_50w, 1)
    returns_50w[0] = 0
    value_50w = initial_investment * np.cumprod(1 + returns_50w)
    logging.info(f"50WMA Strategy final value: ${value_50w[-1]:.2f}")

    # Log position changes for 50WMA
    position_changes_50w = np.diff(position_50w.astype(int))
    num_trades_50w = np.sum(np.abs(position_changes_50w))
    logging.info(f"Number of 50WMA trades: {num_trades_50w}")

    # Calculate and log total returns
    total_return_hold = (buy_hold[-1] / initial_investment - 1) * 100
    total_return_200 = (value_200[-1] / initial_investment - 1) * 100
    total_return_50w = (value_50w[-1] / initial_investment - 1) * 100
    
    logging.info(f"Total returns:")
    logging.info(f"Buy & Hold: {total_return_hold:.2f}%")
    logging.info(f"200DMA: {total_return_200:.2f}%")
    logging.info(f"50WMA: {total_return_50w:.2f}%")

    # Plot
    plt.figure(figsize=(15, 8))
    plt.plot(dates, buy_hold, label='Buy & Hold', color='black', linewidth=5)
    plt.plot(dates, value_200, label='200DMA Strategy', color='green', linestyle='--', linewidth=5)
    plt.plot(dates, value_50w, label='50WMA Strategy', color='red', linestyle='-.', linewidth=5)
    plt.title(f'{ticker}: $1000 Investment - Buy & Hold vs Moving Average Strategies', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    if len(sys.argv) != 2:
        print_usage()
    
    ticker = sys.argv[1]
    analyze_asset(ticker)

if __name__ == "__main__":
    main() 