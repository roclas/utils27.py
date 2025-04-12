#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Download 10 years of Gold data (using GLD ETF as a proxy)
gold = yf.download("GLD", start="2014-04-01", end="2024-04-01", progress=False)
dates = np.array(gold.index)
prices = np.array(gold['Close']).flatten()

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

# Buy and Hold strategy
buy_hold = initial_investment * np.cumprod(1 + daily_returns)

# 200DMA Strategy
position_200 = prices > ma_200
returns_200 = daily_returns * np.roll(position_200, 1)
returns_200[0] = 0
value_200 = initial_investment * np.cumprod(1 + returns_200)

# 50WMA Strategy
position_50w = prices > ma_50w
returns_50w = daily_returns * np.roll(position_50w, 1)
returns_50w[0] = 0
value_50w = initial_investment * np.cumprod(1 + returns_50w)

# Plot
plt.figure(figsize=(15, 8))
plt.plot(dates, buy_hold, label='Buy & Hold', color='black', linewidth=5)
plt.plot(dates, value_200, label='200DMA Strategy', color='green', linestyle='--', linewidth=5)
plt.plot(dates, value_50w, label='50WMA Strategy', color='red', linestyle='-.', linewidth=5)
plt.title('Gold: $1000 Investment - Buy & Hold vs Moving Average Strategies', fontsize=16)
plt.xlabel('Date')
plt.ylabel('Portfolio Value ($)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show() 