#!/usr/bin/python3

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import requests
import numpy as np

# Configuration Constants

# Market Analysis Constants
SIGNIFICANT_DEVIATION_PCT = 5.0  # Percentage threshold for significant deviation from 200DMA
SP500_MARKET_SHARE = 0.8  # S&P 500 represents ~80% of total market cap
BUFFETT_INDICATOR_THRESHOLDS = {
    "SIGNIFICANTLY_OVERVALUED": 120,
    "MODERATELY_OVERVALUED": 100
}

# Asset Symbols
assets = {
    "Bitcoin": "BTC-USD",
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Copper": "HG=F",
    "Nasdaq": "^IXIC",
    "S&P 500": "^GSPC",
    "Crude Oil": "CL=F",
    "China A50": "FXI",         # iShares China Large-Cap ETF
    "South Africa Top 40": "EZA",
    "US Total Market": "VTI"    # Vanguard Total Stock Market ETF
}

# Update GDP constants
GDP_DATA = {
    "US": {
        "value": 26.91,  # Q4 2023 GDP in trillions (latest actual data)
        "date": "2023-Q4"
    },
    "China": {
        "value": 17.52,  # 2023 GDP in trillions USD (latest actual data)
        "date": "2023"
    }
}

def fetch_adaptive_ma_comparison(symbol):
    try:
        # Get 2 years of data to ensure enough history for calculations
        period = "2y"
        data = yf.download(symbol, period=period, auto_adjust=True, progress=False)
        if len(data) == 0:
            return f"{symbol}: No data available ⚠️"
        if len(data) < 200:
            return f"{symbol}: Not enough data (need 200 days, got {len(data)} days) ⚠️"
            
        # Convert to numpy arrays
        prices = data['Close'].values.flatten()
        
        # Calculate rolling std using numpy
        rolling_std = np.zeros(len(prices))
        for i in range(len(prices)):
            start = max(0, i-200)
            rolling_std[i] = np.std(prices[start:i+1]) if i > 0 else 0
            
        # Calculate adaptive window
        adj_window = np.maximum(200 - (rolling_std * 2), 20)
        adj_window = adj_window.astype(int)
        
        # Calculate adaptive MA
        adaptive_ma = np.zeros(len(prices))
        for i in range(len(prices)):
            if i == 0:
                adaptive_ma[i] = prices[0]
            else:
                w = int(adj_window[i])
                start = max(0, i-w)
                adaptive_ma[i] = np.mean(prices[start:i])
        
        # Get latest values
        yesterday_close = prices[-1]
        current_ma = adaptive_ma[-1]
        
        # Calculate Mayer Multiple
        mayer_multiple = yesterday_close / current_ma
        
        if not np.isfinite(current_ma):
            return f"{symbol}: Unable to calculate Adaptive MA (insufficient data) ⚠️"
            
        diff_pct = (yesterday_close - current_ma) / current_ma * 100
        direction = "above" if yesterday_close > current_ma else "below"
        
        # Calculate volatility adjustment
        daily_returns = np.diff(prices) / prices[:-1]
        vol_30d = np.std(daily_returns[-30:]) if len(daily_returns) >= 30 else np.std(daily_returns)
        vol_adjustment = 0.20 / vol_30d if vol_30d > 0 else 1
        vol_adjustment = min(max(vol_adjustment, 0.5), 2)
        
        # Combine Mayer Multiple with volatility for market condition
        if mayer_multiple > 2.4 and vol_adjustment < 1:
            position = "🔴 (High Risk)"
        elif mayer_multiple < 0.9 and vol_adjustment > 1:
            position = "🟢 (Low Risk)"
        else:
            position = "🟡 (Neutral)"
            
        # Add emojis based on direction and percentage
        if direction == "above":
            indicator = "🟢" if diff_pct > SIGNIFICANT_DEVIATION_PCT else "🟡"
        else:
            indicator = "🔴" if abs(diff_pct) > SIGNIFICANT_DEVIATION_PCT else "🟡"
            
        # Special handling for Bitcoin to maintain 50WMA compatibility
        if symbol == "BTC-USD":
            # Calculate 50 week MA (50 * 7 = 350 days)
            wma = np.zeros(len(prices))
            for i in range(len(prices)):
                start = max(0, i-350)
                wma[i] = np.mean(prices[start:i+1])
            
            current_wma = wma[-1]
            if np.isfinite(current_wma):
                diff_pct_50w = (yesterday_close - current_wma) / current_wma * 100
                direction_50w = "above" if yesterday_close > current_wma else "below"
                if direction_50w == "above":
                    indicator_50w = "🟢" if diff_pct_50w > SIGNIFICANT_DEVIATION_PCT else "🟡"
                else:
                    indicator_50w = "🔴" if abs(diff_pct_50w) > SIGNIFICANT_DEVIATION_PCT else "🟡"
                return f"{indicator}{indicator_50w} Yesterday's Close = {yesterday_close:.2f}, AMA = {current_ma:.2f}, {abs(diff_pct):.2f}% {direction} {position}, 50WMA = {current_wma:.2f}, {abs(diff_pct_50w):.2f}% {direction_50w}"
            
        return f"{indicator} Yesterday's Close = {yesterday_close:.2f}, AMA = {current_ma:.2f}, {abs(diff_pct):.2f}% {direction} {position}"
    except Exception as e:
        return f"Error - {str(e)} ⚠️"

def fetch_buffett_indicator(country="US"):
    try:
        if country == "US":
            # Use NYSE data for total market cap
            nyse = yf.download("^NYA", period="1d", auto_adjust=True, progress=False)
            nasdaq = yf.download("^IXIC", period="1d", auto_adjust=True, progress=False)
            
            if nyse.empty or nasdaq.empty:
                return f"{country} Buffett Indicator: No market data available ⚠️"
            
            # NYSE market cap (each point ≈ $1.2B) + NASDAQ market cap (each point ≈ $0.8B)
            total_market_cap = (float(nyse['Close'].values[-1]) * 1.2e9 + 
                              float(nasdaq['Close'].values[-1]) * 0.8e9)
            current_gdp = GDP_DATA["US"]["value"] * 1e12
            gdp_date = GDP_DATA["US"]["date"]
            
        elif country == "China":
            # Use Shanghai Composite Index for China
            ssec = yf.download("000001.SS", period="1d", auto_adjust=True, progress=False)
            szse = yf.download("399001.SZ", period="1d", auto_adjust=True, progress=False)
            if ssec.empty or szse.empty:
                return "China Buffett Indicator: No market data available ⚠️"
            
            # Shanghai + Shenzhen market cap (in USD)
            # Each SSEC point represents roughly $2.5B USD in total market cap
            # Each SZSE point represents roughly $1.5B USD in total market cap
            total_market_cap = (float(ssec['Close'].values[-1]) * 2.5e9 +
                              float(szse['Close'].values[-1]) * 1.5e9)
            current_gdp = GDP_DATA["China"]["value"] * 1e12
            gdp_date = GDP_DATA["China"]["date"]
        
        buffett_ratio = (total_market_cap / current_gdp) * 100
        
        # Format the numbers
        market_cap_t = float(total_market_cap) / 1e12
        gdp_t = float(current_gdp) / 1e12
        
        # Interpret the ratio
        if buffett_ratio > BUFFETT_INDICATOR_THRESHOLDS["SIGNIFICANTLY_OVERVALUED"]:
            indicator = "🔴 Significantly Overvalued"
        elif buffett_ratio > BUFFETT_INDICATOR_THRESHOLDS["MODERATELY_OVERVALUED"]:
            indicator = "🟡 Moderately Overvalued"
        else:
            indicator = "🟢 Fair/Undervalued"
            
        return f"{country} Buffett Indicator: {float(buffett_ratio):.1f}% {indicator} (Market Cap: ${market_cap_t:.2f}T, GDP: ${gdp_t:.2f}T as of {gdp_date})"
    except Exception as e:
        return f"Error calculating {country} Buffett Indicator - {str(e)} ⚠️"

def main():
    print(f"📊 Market Adaptive MA Check ({datetime.today().strftime('%Y-%m-%d')}) 📊\n")
    
    results = []
    for name, symbol in assets.items():
        result = fetch_adaptive_ma_comparison(symbol)  # Updated function call
        try:
            if "%" in result:
                if symbol == "BTC-USD" and "50WMA" in result:
                    # Extract both percentages for Bitcoin more precisely
                    ama_part = result.split(", 50WMA")[0]
                    wma_part = result.split("50WMA =")[1]
                    
                    # Extract the numbers
                    ama_pct = float(ama_part.split("%")[0].split()[-1])
                    wma_pct = float(wma_part.split("%")[0].split()[-1])
                    
                    # Apply signs
                    if "below" in ama_part:
                        ama_pct = -ama_pct
                    if "below" in wma_part:
                        wma_pct = -wma_pct
                    
                    # Calculate average
                    diff_pct = (ama_pct + wma_pct) / 2
                else:
                    diff_pct = float(result.split("%")[0].split()[-1])
                    if "below" in result:
                        diff_pct = -diff_pct
            else:
                diff_pct = -999  # For error cases
        except Exception as e:
            diff_pct = -999
            
        results.append((name, result, diff_pct))
    
    # Sort results by percentage difference (descending order)
    results.sort(key=lambda x: x[2], reverse=True)
    
    # Print sorted results without debug percentages
    for name, result, _ in results:
        print(f"📌 {name}: {result}")
    
    # Add both US and China Buffett Indicators at the end
    print("\n📊 Market Valuation Metrics")
    print(fetch_buffett_indicator("US"))
    print(fetch_buffett_indicator("China"))

if __name__ == "__main__":
    main()

