import pandas as pd
import talib as ta

df = pd.read_csv("livedata_daywiselivedata2024.csv")

df['close'] = pd.to_numeric(df['close'], errors='coerce')
df['date'] = pd.to_datetime(df['date'])

df = df.sort_values(['symbol', 'date'])
df = df.drop_duplicates(subset=['symbol','date'], keep='last')

# ---- USE TRANSFORM ----
df['RSI_6'] = df.groupby('symbol')['close'].transform(lambda x: ta.RSI(x, timeperiod=6))
df['EMA_20'] = df.groupby('symbol')['close'].transform(lambda x: ta.EMA(x, timeperiod=20))
df['SMA_20'] = df.groupby('symbol')['close'].transform(lambda x: ta.SMA(x, timeperiod=20))

df.to_csv("indicators_all_symbols.csv", index=False)
print("Done!")
