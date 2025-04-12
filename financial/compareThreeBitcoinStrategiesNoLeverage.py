#!/usr/bin/env python3

import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants at the top
COMMISSION_RATE = 0.01
MIN_TRADE_PCT = 0.2  # Only trade if position change is > 1% of portfolio

def calculate_ma(prices, window):
    """Calculate moving average using numpy"""
    ma = np.zeros(len(prices))
    for i in range(len(prices)):
        start = max(0, i-window)
        ma[i] = np.mean(prices[start:i+1])
    return ma

def calculate_positions_and_values(prices, dates, initial_investment=1000, commission=COMMISSION_RATE):
    """Calculate positions and values for all strategies
    
    Args:
        prices: Array of bitcoin prices
        dates: Array of dates
        initial_investment: Initial investment amount in USD
        commission: Trading commission as decimal (0.001 = 0.1%)
    """
    
    # Buy and Hold Strategy (only pays commission once)
    commission_cost = initial_investment * commission
    initial_btc = (initial_investment - commission_cost) / prices[0]
    buy_hold = initial_btc * prices

    # 50WMA (350-day) Strategy
    cash_350 = initial_investment
    btc_350 = 0
    value_350 = np.zeros(len(prices))
    value_350[0] = initial_investment

    ma_350 = calculate_ma(prices, 350)
    for i in range(1, len(prices)):
        if prices[i] > ma_350[i] and cash_350 > 0:
            commission_cost = cash_350 * commission
            btc_350 = (cash_350 - commission_cost) / prices[i]
            cash_350 = 0
        elif prices[i] < ma_350[i] and btc_350 > 0:
            gross_revenue = btc_350 * prices[i]
            commission_cost = gross_revenue * commission
            cash_350 = gross_revenue - commission_cost
            btc_350 = 0
        value_350[i] = cash_350 + (btc_350 * prices[i])

    # Adaptive Strategy
    cash_adaptive = initial_investment
    btc_adaptive = 0
    value_adaptive = np.zeros(len(prices))
    value_adaptive[0] = initial_investment

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
        price_vs_ma = ((prices[i] / adaptive_ma[i]) - 1) * 100
        current_mayer = mayer_multiple[i]
        
        # Determine position size based on Mayer Multiple
        target_position = 0.0  # Default to no position
        
        if prices[i] > adaptive_ma[i]:  # Bullish condition
            if current_mayer < 1.2:  # Strong buy
                target_position = 1.0
            elif current_mayer < 2.4:  # Normal market
                target_position = 1.0
            else:  # Overvalued but still bullish
                target_position = 0.5
        else:  # Bearish condition
            if current_mayer < 0.85:  # Very undervalued
                target_position = 0.5  # Keep some exposure
        
        # Calculate position sizes
        portfolio_value = cash_adaptive + (btc_adaptive * prices[i])
        target_btc = (portfolio_value * target_position) / prices[i]
        
        # Calculate trade size as percentage of portfolio
        trade_size_pct = abs(target_btc - btc_adaptive) * prices[i] / portfolio_value
        
        # Only trade if the change is significant
        if trade_size_pct > MIN_TRADE_PCT:
            if target_btc > btc_adaptive:  # Need to buy more
                # Calculate maximum BTC we can buy accounting for commission
                max_btc_possible = cash_adaptive / (prices[i] * (1 + commission))
                btc_to_buy = min(target_btc - btc_adaptive, max_btc_possible)
                
                gross_cost = btc_to_buy * prices[i]
                commission_cost = gross_cost * commission
                total_cost = gross_cost + commission_cost
                
                if btc_to_buy > 0:  # Only buy if we can buy something
                    percentage = (btc_to_buy * prices[i] / portfolio_value) * 100
                    btc_adaptive += btc_to_buy
                    cash_adaptive -= total_cost
                    logging.info(
                        f"[SIGNAL] Date: {np.datetime_as_string(dates[i], unit='D')} - BUY {percentage:.1f}%\n"
                        f"    Price: ${prices[i]:,.2f}\n"
                        f"    Bought: {btc_to_buy:.8f} BTC\n"
                        f"    Total BTC Holdings: {btc_adaptive:.8f} BTC (${btc_adaptive * prices[i]:,.2f})\n"
                        f"    Cost: ${gross_cost:.2f}\n"
                        f"    Commission: ${commission_cost:.2f}\n"
                        f"    Cash Remaining: ${cash_adaptive:.2f}\n"
                        f"    Mayer Multiple: {current_mayer:.2f}\n"
                        f"    Price vs MA: {price_vs_ma:+.2f}%"
                    )
            elif target_btc < btc_adaptive:  # Need to sell
                btc_to_sell = btc_adaptive - target_btc
                gross_revenue = btc_to_sell * prices[i]
                commission_cost = gross_revenue * commission  # Commission only on the amount being sold
                net_revenue = gross_revenue - commission_cost
                
                if btc_to_sell > 0:  # Only execute trade and apply commission if actual trade happens
                    percentage = (btc_to_sell * prices[i] / portfolio_value) * 100
                    btc_adaptive -= btc_to_sell
                    cash_adaptive += net_revenue
                    logging.info(
                        f"[SIGNAL] Date: {np.datetime_as_string(dates[i], unit='D')} - SELL {percentage:.1f}%\n"
                        f"    Price: ${prices[i]:,.2f}\n"
                        f"    Sold: {btc_to_sell:.8f} BTC\n"
                        f"    Total BTC Holdings: {btc_adaptive:.8f} BTC (${btc_adaptive * prices[i]:,.2f})\n"
                        f"    Revenue: ${gross_revenue:.2f}\n"
                        f"    Commission: ${commission_cost:.2f}\n"
                        f"    Cash Balance: ${cash_adaptive:.2f}\n"
                        f"    Mayer Multiple: {current_mayer:.2f}\n"
                        f"    Price vs MA: {price_vs_ma:+.2f}%"
                    )
        
        value_adaptive[i] = cash_adaptive + (btc_adaptive * prices[i])

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

    initial_investment = 1000  # dollars
    first_btc_price = 224.63  # dollars per BTC
    btc_amount = initial_investment / first_btc_price  # ≈ 4.45 BTC
    buy_hold, value_350, adaptive_value = calculate_positions_and_values(
        prices, dates, initial_investment, commission=COMMISSION_RATE
    )

    # Calculate final returns
    final_return_hold = ((buy_hold[-1] / initial_investment) - 1) * 100
    final_return_350 = ((value_350[-1] / initial_investment) - 1) * 100
    final_return_adaptive = ((adaptive_value[-1] / initial_investment) - 1) * 100

    # Plot results
    plt.figure(figsize=(15, 8))
    plt.plot(dates, buy_hold, 'k-', label=f'Buy & Hold ({final_return_hold:.1f}%)', linewidth=2)
    plt.plot(dates, value_350, 'r-', label=f'50WMA ({final_return_350:.1f}%)', linewidth=2)
    plt.plot(dates, adaptive_value, 'b-', label=f'Adaptive ({final_return_adaptive:.1f}%)', linewidth=2)

    plt.title('Bitcoin Strategy Comparison (No Leverage)\n$1,000 Initial Investment', fontsize=14)
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
    print("STRATEGY COMPARISON RESULTS (NO LEVERAGE)")
    print("="*50)
    print(f"\nInitial Investment: ${initial_investment:,.2f}")
    print(f"\nFinal Values:")
    print(f"Buy & Hold: ${buy_hold[-1]:,.2f} ({final_return_hold:.1f}%)")
    print(f"50WMA: ${value_350[-1]:,.2f} ({final_return_350:.1f}%)")
    print(f"Adaptive: ${adaptive_value[-1]:,.2f} ({final_return_adaptive:.1f}%)")

if __name__ == "__main__":
    main()
