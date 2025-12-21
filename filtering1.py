# FILTER ESSENTIAL COLUMNS - Simplified Analysis

import pandas as pd
import talib 
import numpy as np 

print("FILTERING TO ESSENTIAL COLUMNS ONLY")

# Load your complete analysis file
df = pd.read_csv('stock_analysis_with_indicators.csv')  # Change to your actual filename

print(f"\nOriginal columns: {len(df.columns)}")
print(f"Original data: {len(df)} rows")

# OPTION 1: MINIMAL ESSENTIALS (Best for beginners)

essential_minimal = [
    'date',
    'symbol',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'SMA_20',        # Trend
    'RSI',           # Momentum
    'Signal'         # Trading signal
]

df_minimal = df[essential_minimal]

print("\n📊 OPTION 1: MINIMAL ESSENTIALS (10 columns)")
print("Perfect for: Quick daily checks")
print(f"Columns: {', '.join(essential_minimal)}")
print("\nSample:")
print(df_minimal.tail(5))

df_minimal = df_minimal.round(2)
df_minimal.to_csv('stock_analysis_MINIMAL.csv', index=False)
print("\n✅ Saved: stock_analysis_MINIMAL.csv")

# OPTION 2: STANDARD (Good balance)

essential_standard = [
    'date',
    'symbol',
    'close',
    'volume',
    'SMA_20',
    'SMA_50',
    'RSI',
    'MACD',
    'MACD_Signal',
    'ATR',
    'Signal'
]

df_standard = df[essential_standard]

print("\n\n📈 OPTION 2: STANDARD (11 columns)")
print("Perfect for: Regular trading analysis")
print(f"Columns: {', '.join(essential_standard)}")
print("\nSample:")
print(df_standard.tail(5))

df_standard = df_standard.round(2)
df_standard.to_csv('stock_analysis_STANDARD.csv', index=False)
print("\n✅ Saved: stock_analysis_STANDARD.csv")

# OPTION 3: COMPREHENSIVE (For detailed analysis)

essential_comprehensive = [
    'date',
    'symbol',
    'close',
    'volume',
    'SMA_20',
    'SMA_50',
    'SMA_200',
    'RSI',
    'MACD',
    'MACD_Signal',
    'BB_Upper',
    'BB_Lower',
    'ATR',
    'OBV',
    'Stoch_K',
    'Signal'
]

df_comprehensive = df[essential_comprehensive]

print("\n\n💎 OPTION 3: COMPREHENSIVE (16 columns)")
print("Perfect for: Deep technical analysis")
print(f"Columns: {', '.join(essential_comprehensive)}")
print("\nSample:")
print(df_comprehensive.tail(5))

df_comprehensive = df_comprehensive.round(2)
df_comprehensive.to_csv('stock_analysis_COMPREHENSIVE.csv', index=False)
print("\n✅ Saved: stock_analysis_COMPREHENSIVE.csv")

# OPTION 4: CUSTOM - Choose your own!

print("\n\n🎯 OPTION 4: CUSTOM SELECTION")
print("Uncomment and edit the columns you want:\n")

custom_template = '''
#Edit this list with columns YOU want: '''
my_custom_columns = [
    'date',
    'symbol',
    'close',
    'volume',
    # Add indicators you use:
    'SMA_20',
    'RSI',
    # 'MACD',
    # 'BB_Upper',
    # 'ATR',
    'Signal'
]

df_custom = df[my_custom_columns]

df_custom = df_custom.round(2)
df_custom.to_csv('stock_analysis_CUSTOM.csv', index=False)

print(custom_template)

# WHAT EACH COLUMN MEANS

print("COLUMN EXPLANATION GUIDE")

column_guide = """ 
BASIC DATA:
-----------
date             → Trading date
symbol           → Stock ticker symbol
open/high/low    → Daily price range
close            → Closing price (most important)
volume           → Number of shares traded
ltp              → Last traded price (usually same as close)
previous_closing → Yesterday's close

TREND INDICATORS:
-----------------
SMA_20           → 20-day average (short-term trend)
SMA_50           → 50-day average (medium-term trend)
SMA_200          → 200-day average (long-term trend)
EMA_12/EMA_26    → Faster-reacting averages

MOMENTUM:
---------
RSI              → 0-100 scale (< 30 = oversold, > 70 = overbought)
MACD             → Trend momentum
MACD_Signal      → MACD trigger line
MACD_Hist        → Distance between MACD and signal
Stoch_K/Stoch_D  → Another overbought/oversold indicator

VOLATILITY:
-----------
BB_Upper/Lower   → Bollinger Band boundaries (price range)
BB_Middle        → Middle band (usually 20-day SMA)
ATR              → Average price movement per day

VOLUME:
-------
OBV              → On Balance Volume (money flow)
AD               → Accumulation/Distribution

SIGNALS:
--------
Signal           → BUY/SELL/HOLD recommendation
"""

print(column_guide)

# RECOMMENDATION

print("💡 RECOMMENDATION")

recommendation = """
START HERE:
-----------
Use OPTION 1 (MINIMAL) if you're a beginner
→ Only 10 columns, easy to understand
→ Has everything you need for daily trading

THEN UPGRADE TO:
----------------
Use OPTION 2 (STANDARD) after 1-2 weeks
→ Adds MACD and more moving averages
→ Better signal confirmation

FOR ADVANCED:
-------------
Use OPTION 3 (COMPREHENSIVE) when you're comfortable
→ Full technical analysis
→ Multiple indicator confirmation

COLUMNS TO ALWAYS KEEP:
-----------------------
✓ date, close, volume (basic data)
✓ SMA_20 (trend)
✓ RSI (momentum)
✓ Signal (recommendation)

COLUMNS YOU CAN REMOVE:
-----------------------
✗ id (not needed)
✗ ltp (same as close)
✗ previous_closing (can calculate if needed)
✗ EMA_12, EMA_26 (unless you use MACD deeply)
✗ BB_Middle (same as SMA_20)
✗ MACD_Hist (just MACD - Signal)
✗ AD (OBV is enough for volume analysis)
✗ Stoch_D (Stoch_K is enough)
"""

print(recommendation)

# SUMMARY

print("📋 SUMMARY - FILES CREATED")

summary = '''
#Created 3 filtered CSV files: 

1.stock_analysis_MINIMAL.csv  ({len(essential_minimal)} columns)
#   → Best for beginners
   
2. stock_analysis_STANDARD.csv       ({len(essential_standard)} columns)
 #  → Good for most traders
   
3. stock_analysis_COMPREHENSIVE.csv  ({len(essential_comprehensive)} columns)
#   → For detailed analysis

Choose the one that fits your needs!
Open in Excel or any spreadsheet program.
'''

print(summary)

print("✅ FILTERING COMPLETE!")
print("\nNext: Open the MINIMAL file first and see if it works for you!")