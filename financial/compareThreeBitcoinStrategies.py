#!/usr/bin/env python3

import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_ma(prices, window):
    """Calculate moving average using numpy"""
    ma = np.zeros(len(prices))
    for i in range(len(prices)):
        start = max(0, i-window)
        ma[i] = np.mean(prices[start:i+1])
    return ma

def calculate_positions_and_values(prices, daily_returns, initial_investment=1000):
    """Calculate positions and values for all strategies"""
    
    # Buy and Hold
    buy_hold = initial_investment * np.cumprod(1 + daily_returns)

    # 50WMA (350-day) Strategy
    ma_350 = calculate_ma(prices, 350)
    position_350 = prices > ma_350
    returns_350 = daily_returns * np.roll(position_350, 1)
    returns_350[0] = 0
    value_350 = initial_investment * np.cumprod(1 + returns_350)

    # Adaptive Strategy
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
    position_base = prices > adaptive_ma
    
    position_size = np.ones(len(prices))
    position_size[mayer_multiple > 2.4] = 0.5
    position_size[mayer_multiple < 0.9] = 1.5
    
    # Calculate 30-day rolling volatility
    vol_window = 30
    rolling_vol = np.zeros(len(daily_returns))
    for i in range(len(daily_returns)):
        start = max(0, i-vol_window)
        rolling_vol[i] = np.std(daily_returns[start:i+1]) if i > 0 else 0
    
    vol_adjustment = 0.20 / (rolling_vol + 1e-10)  # Avoid division by zero
    vol_adjustment = np.minimum(vol_adjustment, 2)
    vol_adjustment = np.maximum(vol_adjustment, 0.5)
    
    final_position = position_base * position_size * vol_adjustment
    
    # Add logging for position changes
    prev_position = 0
    for i in range(1, len(prices)):
        current_position = final_position[i]
        if current_position != prev_position:
            price_vs_ma = ((prices[i] / adaptive_ma[i]) - 1) * 100
            window_size = adj_window[i]
            vol_factor = vol_adjustment[i]
            mayer_mult = mayer_multiple[i]
            
            action = "HOLD"
            if current_position > prev_position:
                action = "BUY"
            elif current_position < prev_position:
                action = "SELL"
            
            # Convert numpy.datetime64 to datetime object
            date_str = np.datetime_as_string(dates[i], unit='D')
                
            logging.info(
                f"[SIGNAL] Date: {date_str} - {action} - "
                f"Position Size: {current_position:.2f}\n"
                f"    Price: ${prices[i]:,.2f}\n"
                f"    Adaptive MA ({window_size} days): ${adaptive_ma[i]:,.2f} ({price_vs_ma:+.2f}%)\n"
                f"    Mayer Multiple: {mayer_mult:.2f}\n"
                f"    Volatility Adjustment: {vol_factor:.2f}x"
            )
        
        prev_position = current_position
    
    adaptive_returns = daily_returns * np.roll(final_position, 1)
    adaptive_returns[0] = 0
    adaptive_value = initial_investment * np.cumprod(1 + adaptive_returns)

    return buy_hold, value_350, adaptive_value

def main():
    # Add dates as a global variable for logging
    global dates
    
    # Get data for last 10 years
    end_date = datetime.today()
    start_date = end_date - timedelta(days=3650)
    
    logging.info("Downloading Bitcoin data for the last 10 years...")
    data = yf.download("BTC-USD", start=start_date, end=end_date, progress=False)
    
    if data.empty:
        logging.error("No data available")
        return

    # Fix: Convert both prices and dates to numpy arrays
    prices = data['Close'].to_numpy().flatten()
    dates = data.index.to_numpy()  # Convert pandas index to numpy array
    
    daily_returns = np.diff(prices) / prices[:-1]
    daily_returns = np.insert(daily_returns, 0, 0)

    initial_investment = 1000
    buy_hold, value_350, adaptive_value = calculate_positions_and_values(
        prices, daily_returns, initial_investment
    )

    # Calculate final returns
    final_return_hold = ((buy_hold[-1] / initial_investment) - 1) * 100
    final_return_350 = ((value_350[-1] / initial_investment) - 1) * 100
    final_return_adaptive = ((adaptive_value[-1] / initial_investment) - 1) * 100

    # Plot results using numpy arrays for both x and y
    plt.figure(figsize=(15, 8))
    plt.plot(dates, buy_hold, 'k-', label=f'Buy & Hold ({final_return_hold:.1f}%)', linewidth=2)
    plt.plot(dates, value_350, 'r-', label=f'50WMA ({final_return_350:.1f}%)', linewidth=2)
    plt.plot(dates, adaptive_value, 'b-', label=f'Adaptive ({final_return_adaptive:.1f}%)', linewidth=2)

    plt.title('Bitcoin Strategy Comparison\n$1,000 Initial Investment', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    plt.yscale('log')

    # Add summary text
    summary = (
        f"Final Values:\n"
        f"Buy & Hold: ${buy_hold[-1]:,.2f}\n"
        f"50WMA: ${value_350[-1]:,.2f}\n"
        f"Adaptive: ${adaptive_value[-1]:,.2f}"
    )
    plt.text(0.02, 0.98, summary, 
             transform=plt.gca().transAxes, 
             verticalalignment='top',
             fontfamily='monospace',
             bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.show()

    # Print numerical results
    print("\n" + "="*50)
    print("STRATEGY COMPARISON RESULTS")
    print("="*50)
    print(f"\nInitial Investment: ${initial_investment:,.2f}")
    print(f"\nFinal Values:")
    print(f"Buy & Hold: ${buy_hold[-1]:,.2f} ({final_return_hold:.1f}%)")
    print(f"50WMA: ${value_350[-1]:,.2f} ({final_return_350:.1f}%)")
    print(f"Adaptive: ${adaptive_value[-1]:,.2f} ({final_return_adaptive:.1f}%)")

if __name__ == "__main__":
    main() 