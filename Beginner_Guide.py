# TA-Lib Complete Beginner's Guide

import talib
import numpy as np
import pandas as pd

print("TA-LIB BEGINNER'S GUIDE")

# STEP 1: Understanding the Basics
print("\n\n STEP 1: What is TA-Lib?")
print("TA-Lib = Technical Analysis Library")
print("Used for: Analyzing stock/crypto price data")
print("Contains: 150+ technical indicators (RSI, MACD, Moving Averages, etc.)")

# STEP 2: Sample Data Setup
print("\n\n STEP 2: Creating Sample Price Data")

# In real trading, you'd get this from a CSV or API
# For learning, we'll create realistic sample data
np.random.seed(42)
prices = 100 + np.cumsum(np.random.randn(100) * 2)  # Random walk starting at 100

# Standard OHLC data (Open, High, Low, Close)
close = prices
high = close + np.random.uniform(0, 2, 100)
low = close - np.random.uniform(0, 2, 100)
open_price = close + np.random.uniform(-1, 1, 100)
volume = np.random.randint(1000000, 5000000, 100).astype(float)

print(f"Created {len(close)} data points")
print(f"Price range: ${low.min():.2f} - ${high.max():.2f}")
print(f"Latest close price: ${close[-1]:.2f}")

# STEP 3: Moving Averages (Your First Indicator!)
# STEP 1: Create sample price data first!
np.random.seed(42)
prices = 100 + np.cumsum(np.random.randn(100) * 2)  # 100 price points

close = prices  # Closing prices
high = close + np.random.uniform(0, 2, 100)  # High prices
low = close - np.random.uniform(0, 2, 100)   # Low prices

print(f"Created {len(close)} price points")
print(f"Latest price: ${close[-1]:.2f}")

# STEP 2: Now calculate moving averages

sma_20 = talib.SMA(close, timeperiod=20)
sma_50 = talib.SMA(close, timeperiod=50)

print(f"\n20-day SMA: ${sma_20[-1]:.2f}")
print(f"50-day SMA: ${sma_50[-1]:.2f}")
print(f"Current Price: ${close[-1]:.2f}")

if close[-1] > sma_20[-1]:
    print(" Price above 20-day SMA (Bullish)")
else:
    print(" Price below 20-day SMA (Bearish)")
    
# STEP 4: RSI - Overbought/Oversold
print("\n\n STEP 4: RSI - Is the Price Overbought or Oversold?")
print("-" * 60)

rsi = talib.RSI(close, timeperiod=14)

print(f"Current RSI: {rsi[-1]:.2f}")
print("\nInterpretation:")
if rsi[-1] > 70:
    print("⚠️  RSI > 70: OVERBOUGHT (might go down)")
elif rsi[-1] < 30:
    print("✅ RSI < 30: OVERSOLD (might go up)")
else:
    print("➡️  RSI 30-70: NEUTRAL")

# STEP 5: MACD - Momentum & Trend Changes
print("\n\n STEP 5: MACD - Momentum Indicator")
print("-" * 60)

macd, macd_signal, macd_hist = talib.MACD(close, 
                                           fastperiod=12, 
                                           slowperiod=26, 
                                           signalperiod=9)

print(f"MACD Line: {macd[-1]:.2f}")
print(f"Signal Line: {macd_signal[-1]:.2f}")
print(f"Histogram: {macd_hist[-1]:.2f}")

if macd[-1] > macd_signal[-1]:
    print(" MACD above Signal = BULLISH")
else:
    print(" MACD below Signal = BEARISH")

# STEP 6: Bollinger Bands - Volatility
print("\n\n STEP 6: Bollinger Bands - Price Boundaries")
print("-" * 60)

upper, middle, lower = talib.BBANDS(close, timeperiod=20)

print(f"Upper Band: ${upper[-1]:.2f}")
print(f"Middle Band: ${middle[-1]:.2f}")
print(f"Lower Band: ${lower[-1]:.2f}")
print(f"Current Price: ${close[-1]:.2f}")

if close[-1] > upper[-1]:
    print("  Price above upper band (Overbought)")
elif close[-1] < lower[-1]:
    print(" Price below lower band (Oversold)")
else:
    print("  Price within bands (Normal)")

# STEP 7: ATR - Volatility Measurement
print("\n\n STEP 7: ATR - How Volatile is the Market?")
print("-" * 60)

atr = talib.ATR(high, low, close, timeperiod=14)

print(f"Average True Range (ATR): ${atr[-1]:.2f}")
print(f"This means the price typically moves ${atr[-1]:.2f} per day")
print("\nUse for: Position sizing & stop-loss placement")

# STEP 8: Volume Indicators
print("\n\n STEP 8: Volume Analysis")
print("-" * 60)

obv = talib.OBV(close, volume)
print(f"On Balance Volume (OBV): {obv[-1]:,.0f}")
print("Rising OBV = Money flowing IN (bullish)")
print("Falling OBV = Money flowing OUT (bearish)")

# STEP 9: Putting It All Together - Simple Strategy Example
print("\n\n STEP 9: Simple Trading Strategy Example")
print("-" * 60)

def simple_strategy(close, rsi, macd, macd_signal):
    """
    Simple strategy combining RSI and MACD
    """
    signals = []
    
    # Check last 5 data points
    for i in range(-5, 0):
        signal = "HOLD"
        
        # BUY conditions
        if rsi[i] < 30 and macd[i] > macd_signal[i]:
            signal = "BUY"
        
        # SELL conditions
        elif rsi[i] > 70 and macd[i] < macd_signal[i]:
            signal = "SELL"
        
        signals.append({
            'index': i,
            'price': close[i],
            'rsi': rsi[i],
            'signal': signal
        })
    
    return signals

signals = simple_strategy(close, rsi, macd, macd_signal)

print("\nLast 5 trading signals:")
for s in signals:
    print(f"Price: ${s['price']:.2f} | RSI: {s['rsi']:.2f} | Signal: {s['signal']}")

# STEP 10: Working with Real Data (Pandas)
print("\n\n STEP 10: Using TA-Lib with Pandas DataFrames")
print("-" * 60)

# Create a DataFrame (how you'd work with real CSV data)
df = pd.DataFrame({
    'open': open_price,
    'high': high,
    'low': low,
    'close': close,
    'volume': volume
})

# Add indicators to DataFrame
df['SMA_20'] = talib.SMA(df['close'].values, timeperiod=20)
df['RSI'] = talib.RSI(df['close'].values, timeperiod=14)
df['ATR'] = talib.ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=14)

print("\nDataFrame with indicators:")
print(df.tail(5))  # Show last 5 rows

# BONUS: List of Essential Functions to Learn Next

print("\n\n BONUS: Functions to Learn Next")
print("-" * 60)

essential_functions = {
    "Trend": ["SMA", "EMA", "WMA", "DEMA", "TEMA"],
    "Momentum": ["RSI", "MACD", "STOCH", "CCI", "MOM"],
    "Volatility": ["ATR", "BBANDS", "NATR"],
    "Volume": ["OBV", "AD", "ADOSC", "MFI"],
    "Pattern": ["CDL2CROWS", "CDL3BLACKCROWS", "CDLDOJI"]
}

for category, functions in essential_functions.items():
    print(f"\n{category}:")
    print(f"  {', '.join(functions)}")

print("\n\n" + "=" * 60)
print("🎉 CONGRATULATIONS! You've completed the TA-Lib basics!")
print("=" * 60)
print("\nNext Steps:")
print("1. Try these indicators with real stock data")
print("2. Combine 2-3 indicators to create your own strategy")
print("3. Backtest your strategy on historical data")
print("4. Learn pattern recognition functions (CDL*)")
print("\nHappy Trading! ")
