import pandas as pd
import talib

# -------------------------------
# Step 1: Load CSV
# -------------------------------
df = pd.read_csv('daywise_ordered.csv')

# Ensure the necessary columns exist
required_cols = ['date', 'close', 'open', 'high', 'low', 'volume']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in CSV!")

# -------------------------------
# Step 2: Sort by date ascending
# -------------------------------
df = df.sort_values('date').reset_index(drop=True)

# -------------------------------
# Step 3: Calculate Indicators
# -------------------------------

# RSI (14 periods)
df['RSI_14'] = talib.RSI(df['close'], timeperiod=14)

# Simple Moving Average (SMA)
df['SMA_5'] = talib.SMA(df['close'], timeperiod=5)
df['SMA_20'] = talib.SMA(df['close'], timeperiod=20)

# Exponential Moving Average (EMA)
df['EMA_5'] = talib.EMA(df['close'], timeperiod=5)
df['EMA_20'] = talib.EMA(df['close'], timeperiod=20)

# -------------------------------
# Step 4: Optional - Fill NaN with 0 or keep NaN
# -------------------------------
# df.fillna(0, inplace=True)  # Only if you want to replace NaN

# -------------------------------
# Step 5: Save cleaned CSV with indicators
# -------------------------------
df.to_csv('stocks_with_indicators2.csv', index=False)

print("Indicators calculated and CSV saved: stocks_with_indicators.csv")
