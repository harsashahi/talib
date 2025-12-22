# TA-Lib Analysis with Real CSV Data

import talib
import pandas as pd
import numpy as np

print("ANALYZING YOUR STOCK CSV DATA WITH TA-LIB")

# STEP 1: Load Your CSV File
print("\n STEP 1: Loading CSV Data")

# Replace 'your_file.csv' with your actual filename
df = pd.read_csv('daywise_ordered.csv')

print(f" Loaded {len(df)} rows of data")
print(f"Columns: {list(df.columns)}")
print(f"\nFirst few rows:")
print(df.head())

# STEP 2: Data Preparation
# -------------------------
print("\n\n STEP 2: Preparing Data")

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by date (oldest first - important for TA!)
df = df.sort_values('date').reset_index(drop=True)

# Check for missing values
print(f"Missing values:\n{df.isnull().sum()}")

# Remove any rows with missing OHLC data
df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])

print(f"\n Clean data: {len(df)} rows")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")

# STEP 3: Basic Price Statistics
print("\n\n STEP 3: Basic Statistics")

print(f"Symbol: {df['symbol'].iloc[0] if 'symbol' in df else 'N/A'}")
print(f"\nPrice Statistics:")
print(f"  Current Price: ${df['close'].iloc[-1]:.2f}")
print(f"  Previous Close: ${df['previous_closing'].iloc[-1]:.2f}")
print(f"  Change: ${df['close'].iloc[-1] - df['previous_closing'].iloc[-1]:.2f}")
print(f"  Change %: {((df['close'].iloc[-1] / df['previous_closing'].iloc[-1]) - 1) * 100:.2f}%")
print(f"\n  Highest: ${df['high'].max():.2f}")
print(f"  Lowest: ${df['low'].min():.2f}")
print(f"  Average Close: ${df['close'].mean():.2f}")
print(f"  Total Volume: {df['volume'].sum():,.0f}")

# STEP 4: Add Moving Averages
print("\n\n STEP 4: Moving Averages (Trend Analysis)")

df['SMA_20'] = talib.SMA(df['close'].values, timeperiod=20)
df['SMA_50'] = talib.SMA(df['close'].values, timeperiod=50)
df['SMA_200'] = talib.SMA(df['close'].values, timeperiod=200)
df['EMA_12'] = talib.EMA(df['close'].values, timeperiod=12)
df['EMA_26'] = talib.EMA(df['close'].values, timeperiod=26)

print(f"20-day SMA: ${df['SMA_20'].iloc[-1]:.2f}")
print(f"50-day SMA: ${df['SMA_50'].iloc[-1]:.2f}")
print(f"200-day SMA: ${df['SMA_200'].iloc[-1]:.2f}")

# Trend analysis
current_price = df['close'].iloc[-1]
if pd.notna(df['SMA_20'].iloc[-1]) and pd.notna(df['SMA_50'].iloc[-1]):
    if current_price > df['SMA_20'].iloc[-1] > df['SMA_50'].iloc[-1]:
        print("\n✅ STRONG UPTREND: Price > 20 SMA > 50 SMA")
    elif current_price < df['SMA_20'].iloc[-1] < df['SMA_50'].iloc[-1]:
        print("\n❌ STRONG DOWNTREND: Price < 20 SMA < 50 SMA")
    else:
        print("\n➡️  MIXED TREND: Consolidating")

# STEP 5: Add RSI (Momentum)
print("\n\n💪 STEP 5: RSI - Momentum Indicator")

df['RSI'] = talib.RSI(df['close'].values, timeperiod=14)

print(f"Current RSI: {df['RSI'].iloc[-1]:.2f}")

if df['RSI'].iloc[-1] > 70:
    print("⚠️  OVERBOUGHT (RSI > 70) - Potential sell signal")
elif df['RSI'].iloc[-1] < 30:
    print("✅ OVERSOLD (RSI < 30) - Potential buy signal")
else:
    print("➡️  NEUTRAL (RSI 30-70)")

# STEP 6: Add MACD
print("\n\n🎯 STEP 6: MACD - Trend & Momentum")

df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(
    df['close'].values, 
    fastperiod=12, 
    slowperiod=26, 
    signalperiod=9
)

print(f"MACD: {df['MACD'].iloc[-1]:.2f}")
print(f"Signal: {df['MACD_Signal'].iloc[-1]:.2f}")
print(f"Histogram: {df['MACD_Hist'].iloc[-1]:.2f}")

if df['MACD'].iloc[-1] > df['MACD_Signal'].iloc[-1]:
    print("✅ BULLISH: MACD above signal line")
else:
    print("❌ BEARISH: MACD below signal line")

# STEP 7: Add Bollinger Bands
print("\n\n📊 STEP 7: Bollinger Bands - Volatility")

df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = talib.BBANDS(
    df['close'].values, 
    timeperiod=20,
    nbdevup=2,
    nbdevdn=2
)

print(f"Upper Band: ${df['BB_Upper'].iloc[-1]:.2f}")
print(f"Middle Band: ${df['BB_Middle'].iloc[-1]:.2f}")
print(f"Lower Band: ${df['BB_Lower'].iloc[-1]:.2f}")
print(f"Current Price: ${df['close'].iloc[-1]:.2f}")

# Band position
band_position = (df['close'].iloc[-1] - df['BB_Lower'].iloc[-1]) / \
                (df['BB_Upper'].iloc[-1] - df['BB_Lower'].iloc[-1]) * 100

print(f"Band Position: {band_position:.1f}%")

if df['close'].iloc[-1] > df['BB_Upper'].iloc[-1]:
    print("⚠️  Price ABOVE upper band (Overbought)")
elif df['close'].iloc[-1] < df['BB_Lower'].iloc[-1]:
    print("✅ Price BELOW lower band (Oversold)")
else:
    print("➡️  Price within bands")

# STEP 8: Add ATR (Volatility)
print("\n\n📉 STEP 8: ATR - Average True Range")

df['ATR'] = talib.ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=14)

print(f"ATR (14): ${df['ATR'].iloc[-1]:.2f}")
print(f"ATR as % of price: {(df['ATR'].iloc[-1] / df['close'].iloc[-1] * 100):.2f}%")
print("\n💡 Use ATR for:")
print("  - Stop loss: Current price ± (2 × ATR)")
print("  - Position sizing: Risk / ATR")

# STEP 9: Add Volume Indicators
print("\n\n📦 STEP 9: Volume Analysis")

df['OBV'] = talib.OBV(df['close'].values, df['volume'].values.astype(float))
df['AD'] = talib.AD(df['high'].values, df['low'].values, df['close'].values, df['volume'].values.astype(float))

print(f"On Balance Volume (OBV): {df['OBV'].iloc[-1]:,.0f}")
print(f"Accumulation/Distribution: {df['AD'].iloc[-1]:,.0f}")

# OBV trend
obv_change = df['OBV'].iloc[-1] - df['OBV'].iloc[-10]
if obv_change > 0:
    print("✅ OBV Rising: Money flowing IN (bullish)")
else:
    print("❌ OBV Falling: Money flowing OUT (bearish)")

# STEP 10: Add Stochastic Oscillator
print("\n\n🎲 STEP 10: Stochastic Oscillator")

df['Stoch_K'], df['Stoch_D'] = talib.STOCH(
    df['high'].values,
    df['low'].values,
    df['close'].values,
    fastk_period=14,
    slowk_period=3,
    slowd_period=3
)

print(f"Stochastic %K: {df['Stoch_K'].iloc[-1]:.2f}")
print(f"Stochastic %D: {df['Stoch_D'].iloc[-1]:.2f}")

if df['Stoch_K'].iloc[-1] > 80:
    print("⚠️  OVERBOUGHT (>80)")
elif df['Stoch_K'].iloc[-1] < 20:
    print("✅ OVERSOLD (<20)")
else:
    print("➡️  NEUTRAL")

# STEP 11: Trading Signals
print("\n\n🚦 STEP 11: Simple Trading Signals")

def generate_signal(row):
    """Generate buy/sell/hold signal based on multiple indicators"""
    signals = []
    
    # RSI signal
    if pd.notna(row['RSI']):
        if row['RSI'] < 30:
            signals.append('BUY')
        elif row['RSI'] > 70:
            signals.append('SELL')
    
    # MACD signal
    if pd.notna(row['MACD']) and pd.notna(row['MACD_Signal']):
        if row['MACD'] > row['MACD_Signal']:
            signals.append('BUY')
        else:
            signals.append('SELL')
    
    # Moving Average signal
    if pd.notna(row['SMA_20']) and pd.notna(row['SMA_50']):
        if row['close'] > row['SMA_20'] > row['SMA_50']:
            signals.append('BUY')
        elif row['close'] < row['SMA_20'] < row['SMA_50']:
            signals.append('SELL')
    
    # Count signals
    buy_count = signals.count('BUY')
    sell_count = signals.count('SELL')
    
    if buy_count > sell_count:
        return 'BUY'
    elif sell_count > buy_count:
        return 'SELL'
    else:
        return 'HOLD'

df['Signal'] = df.apply(generate_signal, axis=1)

print(f"Current Signal: {df['Signal'].iloc[-1]}")
print(f"\nLast 10 signals:")
print(df[['date', 'close', 'RSI', 'Signal']].tail(10).to_string(index=False))

# STEP 12: Save Results
print("\n\n💾 STEP 12: Saving Analysis")

# Save full analysis to new CSV
output_file = 'stock_analysis_with_indicators_new.csv'
df.to_csv(output_file, index=False)
print(f"✅ Saved full analysis to: {output_file}")

# Save just the summary
summary_df = df[['date', 'symbol', 'close', 'SMA_20', 'SMA_50', 'RSI', 'MACD', 'Signal']].tail(30)
summary_df.to_csv('stock_summary_last_30_days.csv', index=False)

# STEP 13: Key Statistics Summary
print("\n\n📋 STEP 13: Final Summary")

print(f"""
STOCK ANALYSIS SUMMARY

Symbol: {df['symbol'].iloc[0] if 'symbol' in df else 'N/A'}
Current Price: ${df['close'].iloc[-1]:.2f}
Previous Close: ${df['previous_closing'].iloc[-1]:.2f}
Change: {((df['close'].iloc[-1] / df['previous_closing'].iloc[-1]) - 1) * 100:+.2f}%

TECHNICAL INDICATORS:

RSI (14): {df['RSI'].iloc[-1]:.2f} {'[OVERBOUGHT]' if df['RSI'].iloc[-1] > 70 else '[OVERSOLD]' if df['RSI'].iloc[-1] < 30 else '[NEUTRAL]'}
MACD: {df['MACD'].iloc[-1]:.2f}
Signal: {df['MACD_Signal'].iloc[-1]:.2f}
ATR: ${df['ATR'].iloc[-1]:.2f}

MOVING AVERAGES:

20-day SMA: ${df['SMA_20'].iloc[-1]:.2f}
50-day SMA: ${df['SMA_50'].iloc[-1]:.2f}
200-day SMA: ${df['SMA_200'].iloc[-1]:.2f}

TRADING SIGNAL: {df['Signal'].iloc[-1]}
""")

print("🎉 ANALYSIS COMPLETE!")
print("\nNext Steps:")
print("1. Review the generated CSV files")
print("2. Backtest your strategy on historical data")
print("3. Adjust indicator parameters based on your trading style")
print("4. Consider adding more indicators (ADX, CCI, etc.)")
print("5. Build a dashboard to visualize the data")