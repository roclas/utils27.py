#!/usr/bin/env python3

import numpy as np
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging
from tqdm import tqdm
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class StrategyResult:
    def __init__(self):
        self.wins = 0
        self.total_windows = 0
        self.return_differences = []
        self.win_margins = []
        self.loss_margins = []
        
    def add_result(self, strategy_return: float, buy_hold_return: float):
        self.total_windows += 1
        diff = strategy_return - buy_hold_return
        self.return_differences.append(diff)
        
        if diff > 0:
            self.wins += 1
            self.win_margins.append(diff)
        elif diff < 0:
            self.loss_margins.append(abs(diff))

    def get_stats(self) -> Dict:
        win_rate = (self.wins / self.total_windows) * 100 if self.total_windows > 0 else 0
        avg_win_margin = np.mean(self.win_margins) if self.win_margins else 0
        avg_loss_margin = np.mean(self.loss_margins) if self.loss_margins else 0
        avg_overall_diff = np.mean(self.return_differences)
        
        return {
            'win_rate': win_rate,
            'total_windows': self.total_windows,
            'wins': self.wins,
            'avg_win_margin': avg_win_margin,
            'avg_loss_margin': avg_loss_margin,
            'avg_overall_diff': avg_overall_diff
        }

def calculate_strategy_returns(prices: np.array) -> Tuple[float, float, float, float]:
    """Calculate returns for different strategies"""
    if len(prices) < 2:
        return 0, 0, 0, 0
        
    # Ensure prices is a 1D array
    prices = np.array(prices).flatten()
    
    # Calculate daily returns
    daily_returns = np.diff(prices) / prices[:-1]
    daily_returns = np.insert(daily_returns, 0, 0)
    
    # Buy and Hold
    buy_hold = np.cumprod(1 + daily_returns)
    buy_hold_return = (buy_hold[-1] - 1) * 100

    # 200DMA Strategy
    ma_200 = np.zeros(len(prices))
    for i in range(len(prices)):
        start = max(0, i-200)
        ma_200[i] = np.mean(prices[start:i+1])
    
    position_200 = prices > ma_200
    returns_200 = daily_returns * np.roll(position_200, 1)
    returns_200[0] = 0
    value_200 = np.cumprod(1 + returns_200)
    ma_200_return = (value_200[-1] - 1) * 100

    # 50WMA (350-day) Strategy
    ma_350 = np.zeros(len(prices))
    for i in range(len(prices)):
        start = max(0, i-350)
        ma_350[i] = np.mean(prices[start:i+1])
    
    position_350 = prices > ma_350
    returns_350 = daily_returns * np.roll(position_350, 1)
    returns_350[0] = 0
    value_350 = np.cumprod(1 + returns_350)
    ma_350_return = (value_350[-1] - 1) * 100

    # Adaptive Strategy
    rolling_std = pd.Series(prices).rolling(window=200).std()
    adj_window = np.maximum(200 - (rolling_std * 2).fillna(0), 20)
    adj_window = adj_window.astype(int)
    
    adaptive_ma = np.zeros(len(prices))
    for i in range(len(prices)):
        if i == 0:
            adaptive_ma[i] = prices[0]
        else:
            w = int(adj_window[i])
            start = max(0, i-w)
            adaptive_ma[i] = np.mean(prices[start:i])
    
    mayer_multiple = prices / adaptive_ma
    position_base = prices > adaptive_ma
    
    position_size = np.ones(len(prices))
    position_size[mayer_multiple > 2.4] = 0.5
    position_size[mayer_multiple < 0.9] = 1.5
    
    rolling_vol = pd.Series(daily_returns).rolling(window=30).std().fillna(0)
    vol_adjustment = 0.20 / rolling_vol
    vol_adjustment = np.minimum(vol_adjustment, 2)
    vol_adjustment = np.maximum(vol_adjustment, 0.5)
    
    final_position = position_base * position_size * vol_adjustment
    adaptive_returns = daily_returns * np.roll(final_position, 1)
    adaptive_returns[0] = 0
    adaptive_value = np.cumprod(1 + adaptive_returns)
    adaptive_return = (adaptive_value[-1] - 1) * 100

    return buy_hold_return, ma_200_return, ma_350_return, adaptive_return

def analyze_rolling_windows(ticker: str = "BTC-USD"):
    # Get data for last 10 years
    end_date = datetime.today()
    start_date = end_date - timedelta(days=3650)
    
    logging.info(f"Downloading data for {ticker} from {start_date.date()} to {end_date.date()}")
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    
    if data.empty:
        logging.error(f"No data available for {ticker}")
        return None

    prices = data['Close'].values
    dates = data.index

    # Initialize results
    ma_200_results = StrategyResult()
    ma_350_results = StrategyResult()
    adaptive_results = StrategyResult()

    # 5-year window in trading days (approximate)
    window_days = 252 * 5
    
    # Ensure we have enough data
    if len(prices) < window_days:
        logging.error(f"Not enough data. Need at least {window_days} days.")
        return None
    
    logging.info("Analyzing rolling windows...")
    
    # Analyze each window
    for i in tqdm(range(len(prices) - window_days + 1)):
        window_prices = prices[i:i+window_days]
        window_dates = dates[i:i+window_days]
        
        buy_hold_return, ma_200_return, ma_350_return, adaptive_return = calculate_strategy_returns(window_prices)
        
        ma_200_results.add_result(ma_200_return, buy_hold_return)
        ma_350_results.add_result(ma_350_return, buy_hold_return)
        adaptive_results.add_result(adaptive_return, buy_hold_return)

    # Print results
    print("\n" + "="*80)
    print(f"ROLLING WINDOW ANALYSIS RESULTS FOR {ticker}")
    print(f"Analysis Period: {start_date.date()} to {end_date.date()}")
    print(f"Window Size: 5 years")
    print("="*80)

    ma_200_stats = ma_200_results.get_stats()
    ma_350_stats = ma_350_results.get_stats()
    adaptive_stats = adaptive_results.get_stats()

    print("\n200DMA Strategy vs Buy & Hold:")
    print(f"Win Rate: {ma_200_stats['win_rate']:.2f}% ({ma_200_stats['wins']}/{ma_200_stats['total_windows']} windows)")
    print(f"Average Win Margin: {ma_200_stats['avg_win_margin']:.2f}%")
    print(f"Average Loss Margin: {ma_200_stats['avg_loss_margin']:.2f}%")
    print(f"Average Overall Difference: {ma_200_stats['avg_overall_diff']:.2f}%")

    print("\n50WMA (350-day) Strategy vs Buy & Hold:")
    print(f"Win Rate: {ma_350_stats['win_rate']:.2f}% ({ma_350_stats['wins']}/{ma_350_stats['total_windows']} windows)")
    print(f"Average Win Margin: {ma_350_stats['avg_win_margin']:.2f}%")
    print(f"Average Loss Margin: {ma_350_stats['avg_loss_margin']:.2f}%")
    print(f"Average Overall Difference: {ma_350_stats['avg_overall_diff']:.2f}%")

    print("\nAdaptive Strategy vs Buy & Hold:")
    print(f"Win Rate: {adaptive_stats['win_rate']:.2f}% ({adaptive_stats['wins']}/{adaptive_stats['total_windows']} windows)")
    print(f"Average Win Margin: {adaptive_stats['avg_win_margin']:.2f}%")
    print(f"Average Loss Margin: {adaptive_stats['avg_loss_margin']:.2f}%")
    print(f"Average Overall Difference: {adaptive_stats['avg_overall_diff']:.2f}%")

    print("\nOVERALL WINNER:")
    best_diff = max(ma_200_stats['avg_overall_diff'], 
                   ma_350_stats['avg_overall_diff'],
                   adaptive_stats['avg_overall_diff'])
    
    if best_diff <= 0:
        print("Buy & Hold (All strategies underperformed)")
    else:
        if best_diff == ma_200_stats['avg_overall_diff']:
            print("200DMA Strategy (Best overall performance)")
        elif best_diff == ma_350_stats['avg_overall_diff']:
            print("50WMA Strategy (Best overall performance)")
        else:
            print("Adaptive Strategy (Best overall performance)")

def main():
    analyze_rolling_windows()

if __name__ == "__main__":
    main() 