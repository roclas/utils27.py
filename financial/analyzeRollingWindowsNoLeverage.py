#!/usr/bin/env python3

import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

# Add this constant at the top of the file, after the imports
COMMISSION = 0.00  # 0% commission by default, can be modified (e.g., 0.05 for 5%)

def calculate_ma(prices, window):
    """Calculate moving average using numpy"""
    ma = np.zeros(len(prices))
    for i in range(len(prices)):
        start = max(0, i-window)
        ma[i] = np.mean(prices[start:i+1])
    return ma

def calculate_returns_for_window(prices, dates, initial_investment=1000):
    """Calculate returns for all strategies in a given window"""
    
    # Buy and Hold Strategy (only pays commission once when buying)
    initial_btc = (initial_investment * (1 - COMMISSION)) / prices[0]  # Commission on entry
    buy_hold = initial_btc * prices[-1]

    # 50WMA (350-day) Strategy
    cash_350 = initial_investment
    btc_350 = 0
    ma_350 = calculate_ma(prices, 350)
    
    for i in range(1, len(prices)):
        if prices[i] > ma_350[i] and cash_350 > 0:
            btc_350 = (cash_350 * (1 - COMMISSION)) / prices[i]  # Commission on buy
            cash_350 = 0
        elif prices[i] < ma_350[i] and btc_350 > 0:
            cash_350 = (btc_350 * prices[i]) * (1 - COMMISSION)  # Commission on sell
            btc_350 = 0
    
    value_350 = cash_350 + (btc_350 * prices[-1])

    # Adaptive Strategy
    cash_adaptive = initial_investment
    btc_adaptive = 0

    window = 200
    rolling_std = np.zeros(len(prices))
    for i in range(len(prices)):
        start = max(0, i-window)
        rolling_std[i] = np.std(prices[start:i+1]) if i > 0 else 0
    
    adj_window = np.maximum(window - (rolling_std * 2), 20)
    adj_window = adj_window.astype(int)
    
    adaptive_ma = np.zeros(len(prices))
    for i in range(len(prices)):
        w = int(adj_window[i])
        start = max(0, i-w)
        adaptive_ma[i] = np.mean(prices[start:i+1])
    
    mayer_multiple = prices / adaptive_ma
    
    for i in range(1, len(prices)):
        if prices[i] > adaptive_ma[i]:  # Bullish condition
            if mayer_multiple[i] < 1.2:  # Strong buy
                target_position = 1.0
            elif mayer_multiple[i] < 2.4:  # Normal market
                target_position = 1.0
            else:  # Overvalued but still bullish
                target_position = 0.5
        else:  # Bearish condition
            if mayer_multiple[i] < 0.85:  # Very undervalued
                target_position = 0.5
            else:
                target_position = 0.0
                
        portfolio_value = cash_adaptive + (btc_adaptive * prices[i])
        target_btc = (portfolio_value * target_position) / prices[i]
        
        if target_btc > btc_adaptive:  # Need to buy
            btc_to_buy = target_btc - btc_adaptive
            cost = btc_to_buy * prices[i]
            if cost <= cash_adaptive:
                btc_adaptive += (cost * (1 - COMMISSION)) / prices[i]  # Commission on buy
                cash_adaptive -= cost
        elif target_btc < btc_adaptive:  # Need to sell
            btc_to_sell = btc_adaptive - target_btc
            revenue = btc_to_sell * prices[i]
            btc_adaptive -= btc_to_sell
            cash_adaptive += revenue * (1 - COMMISSION)  # Commission on sell
    
    value_adaptive = cash_adaptive + (btc_adaptive * prices[-1])

    return buy_hold, value_350, value_adaptive

def main():
    # Get data for last 10 years
    end_date = datetime.today()
    start_date = end_date - timedelta(days=3650)
    
    logging.info("Downloading Bitcoin data for the last 10 years...")
    data = yf.download("BTC-USD", start=start_date, end=end_date, progress=False)
    
    if data.empty:
        logging.error("No data available")
        return

    prices = data['Close'].to_numpy().flatten()
    dates = data.index.to_numpy()
    
    # Parameters for rolling windows
    window_size = 5 * 365  # 5 years in days
    initial_investment = 1000
    
    # Arrays to store results
    wins_hold = 0
    wins_350 = 0
    wins_adaptive = 0
    returns_hold = []
    returns_350 = []
    returns_adaptive = []
    
    # Calculate total windows for progress bar
    total_windows = len(prices) - window_size + 1
    
    # Analyze each window with progress bar
    for i in tqdm(range(total_windows), desc="Analyzing windows", unit="window"):
        window_prices = prices[i:i+window_size]
        window_dates = dates[i:i+window_size]
        
        buy_hold, value_350, value_adaptive = calculate_returns_for_window(
            window_prices, window_dates, initial_investment
        )
        
        # Calculate returns
        return_hold = ((buy_hold / initial_investment) - 1) * 100
        return_350 = ((value_350 / initial_investment) - 1) * 100
        return_adaptive = ((value_adaptive / initial_investment) - 1) * 100
        
        returns_hold.append(return_hold)
        returns_350.append(return_350)
        returns_adaptive.append(return_adaptive)
        
        # Count wins
        max_return = max(return_hold, return_350, return_adaptive)
        if max_return == return_hold:
            wins_hold += 1
        elif max_return == return_350:
            wins_350 += 1
        else:
            wins_adaptive += 1
    
    # Print results
    print("\n" + "="*50)
    print("ROLLING 5-YEAR WINDOWS ANALYSIS")
    print("="*50)
    print(f"\nTotal windows analyzed: {total_windows}")
    print("\nWin Count:")
    print(f"Buy & Hold: {wins_hold} ({wins_hold/total_windows*100:.1f}%)")
    print(f"50WMA: {wins_350} ({wins_350/total_windows*100:.1f}%)")
    print(f"Adaptive: {wins_adaptive} ({wins_adaptive/total_windows*100:.1f}%)")
    
    print("\nAverage Returns:")
    print(f"Buy & Hold: {np.mean(returns_hold):.1f}%")
    print(f"50WMA: {np.mean(returns_350):.1f}%")
    print(f"Adaptive: {np.mean(returns_adaptive):.1f}%")
    
    print("\nMedian Returns:")
    print(f"Buy & Hold: {np.median(returns_hold):.1f}%")
    print(f"50WMA: {np.median(returns_350):.1f}%")
    print(f"Adaptive: {np.median(returns_adaptive):.1f}%")
    
    print("\nBest Returns:")
    print(f"Buy & Hold: {np.max(returns_hold):.1f}%")
    print(f"50WMA: {np.max(returns_350):.1f}%")
    print(f"Adaptive: {np.max(returns_adaptive):.1f}%")
    
    print("\nWorst Returns:")
    print(f"Buy & Hold: {np.min(returns_hold):.1f}%")
    print(f"50WMA: {np.min(returns_350):.1f}%")
    print(f"Adaptive: {np.min(returns_adaptive):.1f}%")

if __name__ == "__main__":
    main() 
