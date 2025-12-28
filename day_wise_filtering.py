import pandas as pd
import numpy as np
import talib

#  Load raw data
df = pd.read_csv("daywise_ordered.csv")

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort day-wise per symbol
df = df.sort_values(['symbol', 'date']).reset_index(drop=True)

# Ensure raw columns exist
expected_raw_cols = ['id','date','symbol','open','high','low','close','volume','ltp','previous_closing','serial_no','price','pv']
for col in expected_raw_cols:
    if col not in df.columns:
        df[col] = np.nan

# Save raw_data.csv
df[expected_raw_cols].to_csv("raw_data.csv", index=False)

# Day-wise Filtering / Clean-Up
# Remove rows with missing critical values
df = df.dropna(subset=['close', 'volume'])

# Optional: remove zero volume
df = df[df['volume'] > 0]

df = df.reset_index(drop=True)

# Calculate Indicators
def calculate_indicators(group):
    close = group['close'].values
    high = group['high'].values
    low = group['low'].values
    volume = group['volume'].values

    # SMA, EMA
    group['SMA_20'] = talib.SMA(close, timeperiod=20)
    group['SMA_50'] = talib.SMA(close, timeperiod=50)
    group['EMA_12'] = talib.EMA(close, timeperiod=12)
    group['EMA_26'] = talib.EMA(close, timeperiod=26)

    # MACD
    macd, macd_signal, macd_hist = talib.MACD(close)
    group['MACD'] = macd
    group['MACD_Signal'] = macd_signal
    group['MACD_Hist'] = macd_hist

    # RSI
    group['RSI'] = talib.RSI(close, timeperiod=14)

    # PVVR & Intraday PVVR
    group['pvvr'] = (close * volume).cumsum() / volume.cumsum()
    group['intraday_pvvr'] = ((high + low + close)/3 * volume)

    # Rate & Volume Change (%)
    group['rate_change_pct'] = group['close'].pct_change() * 100
    group['volume_change_pct'] = group['volume'].pct_change() * 100

    return group

df = df.groupby('symbol').apply(calculate_indicators).reset_index(drop=True)

# Round numeric columns
num_cols = df.select_dtypes(include=np.number).columns
df[num_cols] = df[num_cols].round(2)

# Save indicators.csv
indicator_columns = ['SMA_20','SMA_50','EMA_12','EMA_26','MACD','MACD_Signal','MACD_Hist','RSI','pvvr','intraday_pvvr','rate_change_pct','volume_change_pct']
df[indicator_columns].to_csv("indicators.csv", index=False)

# Generate Signals
def generate_signals(row):
    buy_signal = 0
    sell_signal = 0
    score = 0

    # Example logic combining RSI & MACD
    if row['RSI'] < 30 and row['MACD'] > row['MACD_Signal']:
        buy_signal = 1
        score = 2
    elif row['RSI'] > 70 and row['MACD'] < row['MACD_Signal']:
        sell_signal = 1
        score = -2
    elif row['RSI'] < 50 and row['MACD'] > row['MACD_Signal']:
        buy_signal = 1
        score = 1
    elif row['RSI'] > 50 and row['MACD'] < row['MACD_Signal']:
        sell_signal = 1
        score = -1

    return pd.Series([buy_signal, sell_signal, score])

df[['buy_signal','sell_signal','score']] = df.apply(generate_signals, axis=1)

# Rank per day
df['rank'] = df.groupby('date')['score'].rank(ascending=False)

# Save signals.csv
signal_columns = ['buy_signal','sell_signal','score','rank']
df[signal_columns].to_csv("signals.csv", index=False)

print("✅ All CSVs generated successfully!")
