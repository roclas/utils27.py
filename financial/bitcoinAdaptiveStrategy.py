#!/usr/bin/env python3

import numpy as np
import yfinance as yf
import sys
import logging
import pandas as pd
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_volatility_adjusted_ma(prices, window, sensitivity=2):
    """Calculate a volatility-adjusted moving average"""
    # Standard deviation as volatility measure
    rolling_std = pd.Series(prices).rolling(window=window).std()
    # Adjust MA window based on volatility
    adj_window = np.maximum(window - (rolling_std * sensitivity).fillna(0), 20)
    adj_window = adj_window.astype(int)
    
    # Calculate adaptive MA
    ma = np.zeros(len(prices))
    for i in range(len(prices)):
        if i == 0:
            ma[i] = prices[0]
        else:
            w = int(adj_window[i])
            start = max(0, i-w)
            ma[i] = np.mean(prices[start:i])
    return ma

def calculate_mayer_multiple(prices, ma_200):
    """Calculate Mayer Multiple (Price/200DMA)"""
    return prices / ma_200

def calculate_drawdown(values):
    peak = np.maximum.accumulate(values)
    drawdown = (values - peak) / peak
    return np.min(drawdown) * 100

def analyze_bitcoin(start_date=None, end_date=None):
    # If no dates provided, use last 10 years until today
    if start_date is None:
        end_date = datetime.today().strftime('%Y%m%d')
        start_date = (datetime.today() - timedelta(days=3650)).strftime('%Y%m%d')
    
    # Convert YYYYMMDD to YYYY-MM-DD format for yfinance
    start_date = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:]}"
    end_date = f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:]}"
    
    logging.info(f"Analyzing BTC-USD from {start_date} to {end_date}")
    
    # Download data
    data = yf.download("BTC-USD", start=start_date, end=end_date, progress=False)
    if data.empty:
        print(f"\nNo data available for period {start_date} to {end_date}")
        return None
        
    prices = np.array(data['Close']).flatten()
    
    logging.info(f"Data points: {len(prices)}")
    logging.info(f"First price: {prices[0]:.2f}, Last price: {prices[-1]:.2f}")

    initial_investment = 1000

    # Calculate indicators
    ma_200 = calculate_volatility_adjusted_ma(prices, 200)
    mayer_multiple = calculate_mayer_multiple(prices, ma_200)
    
    # Calculate daily returns
    daily_returns = np.diff(prices) / prices[:-1]
    daily_returns = np.insert(daily_returns, 0, 0)

    # Buy and Hold strategy
    buy_hold = initial_investment * np.cumprod(1 + daily_returns)

    # Adaptive Strategy combining:
    # 1. Volatility-adjusted 200MA
    # 2. Mayer Multiple for position sizing
    # 3. Volatility-based risk management
    
    # Base position from MA
    position_base = prices > ma_200
    
    # Adjust position size based on Mayer Multiple
    position_size = np.ones(len(prices))
    position_size[mayer_multiple > 2.4] = 0.5  # Reduce position when overvalued
    position_size[mayer_multiple < 0.9] = 1.5  # Increase position when undervalued
    
    # Calculate 30-day volatility
    rolling_vol = pd.Series(daily_returns).rolling(window=30).std().fillna(0)
    vol_adjustment = 0.20 / rolling_vol  # Target 20% volatility
    vol_adjustment = np.minimum(vol_adjustment, 2)  # Cap leverage at 2x
    vol_adjustment = np.maximum(vol_adjustment, 0.5)  # Minimum position 0.5x
    
    # Combine signals
    final_position = position_base * position_size * vol_adjustment
    
    # Calculate strategy returns
    strategy_returns = daily_returns * np.roll(final_position, 1)
    strategy_returns[0] = 0
    adaptive_value = initial_investment * np.cumprod(1 + strategy_returns)

    # Calculate metrics
    total_return_hold = (buy_hold[-1] / initial_investment - 1) * 100
    total_return_adaptive = (adaptive_value[-1] / initial_investment - 1) * 100
    
    # Calculate position changes
    position_changes = np.diff(final_position)
    num_trades = np.sum(np.abs(position_changes) > 0.1)  # Count significant position changes
    
    logging.info(f"Buy & Hold final value: ${buy_hold[-1]:.2f}")
    logging.info(f"Adaptive Strategy final value: ${adaptive_value[-1]:.2f}")
    logging.info(f"Number of significant position changes: {num_trades}")
    logging.info(f"Total returns:")
    logging.info(f"Buy & Hold: {total_return_hold:.2f}%")
    logging.info(f"Adaptive Strategy: {total_return_adaptive:.2f}%")

    # Calculate max drawdowns
    dd_hold = calculate_drawdown(buy_hold)
    dd_adaptive = calculate_drawdown(adaptive_value)
    
    logging.info(f"Maximum Drawdowns:")
    logging.info(f"Buy & Hold: {dd_hold:.2f}%")
    logging.info(f"Adaptive Strategy: {dd_adaptive:.2f}%")

    # Print results in a clear format
    print("\n" + "="*70)
    print(f"BITCOIN STRATEGY RESULTS")
    print("="*70)
    print(f"Period: {start_date} to {end_date}")
    print(f"\nInitial Investment: ${initial_investment:,.2f}")
    print(f"Buy & Hold Final: ${buy_hold[-1]:,.2f}")
    print(f"Adaptive Final: ${adaptive_value[-1]:,.2f}")
    print(f"\nTotal Returns:")
    print(f"Buy & Hold: {total_return_hold:,.2f}%")
    print(f"Adaptive: {total_return_adaptive:,.2f}%")
    print(f"\nMax Drawdowns:")
    print(f"Buy & Hold: {dd_hold:.2f}%")
    print(f"Adaptive: {dd_adaptive:.2f}%")
    
    print("\n" + "="*70)
    if total_return_adaptive > total_return_hold:
        print(f"WINNER: ADAPTIVE STRATEGY beats Buy & Hold by {(total_return_adaptive - total_return_hold):,.2f}%")
    elif total_return_adaptive < total_return_hold:
        print(f"WINNER: BUY & HOLD beats Adaptive Strategy by {(total_return_hold - total_return_adaptive):,.2f}%")
    else:
        print("TIED: Both strategies performed equally")
    print("="*70 + "\n")

    return {
        'period': f"{start_date} to {end_date}",
        'hold_final': buy_hold[-1],
        'adaptive_final': adaptive_value[-1],
        'hold_return': total_return_hold,
        'adaptive_return': total_return_adaptive,
        'hold_drawdown': dd_hold,
        'adaptive_drawdown': dd_adaptive
    }

def main():
    if len(sys.argv) == 1:
        # No dates provided, use last 10 years
        analyze_bitcoin()
    elif len(sys.argv) == 3:
        # Start and end dates provided
        start_date = sys.argv[1]
        end_date = sys.argv[2]
        
        # Validate date format
        try:
            datetime.strptime(start_date, '%Y%m%d')
            datetime.strptime(end_date, '%Y%m%d')
        except ValueError:
            print("Error: Dates must be in YYYYMMDD format")
            print("Example: python bitcoinAdaptiveStrategy.py 20170101 20241231")
            sys.exit(1)
            
        analyze_bitcoin(start_date, end_date)
    else:
        print("Usage:")
        print("  No dates (last 10 years): python bitcoinAdaptiveStrategy.py")
        print("  Specific period: python bitcoinAdaptiveStrategy.py YYYYMMDD YYYYMMDD")
        print("Example: python bitcoinAdaptiveStrategy.py 20170101 20241231")
        sys.exit(1)

if __name__ == "__main__":
    main() 