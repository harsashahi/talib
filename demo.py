import pandas as pd
import talib as ta

# ---------------------
# Load your CSV data
# ---------------------
df = pd.read_csv("daywise_ordered.csv")

# ---------------------
# Select one symbol
# ---------------------
symbol = "NABIL"  # change this to any symbol you want
symbol_df = df[df['symbol'] == symbol].copy()

# ---------------------
# Sort by date
# ---------------------
symbol_df = symbol_df.sort_values(by='date')

# ---------------------
# Remove duplicate dates
# (Keep latest close of the day)
# ---------------------
symbol_df = symbol_df.drop_duplicates(subset=['date'], keep='last')

# ---------------------
# Ensure numeric close values
# ---------------------
symbol_df['close'] = symbol_df['close'].astype(float)

# ---------------------
# Apply RSI (you can change time period)
# ---------------------
symbol_df['RSI_6'] = ta.RSI(symbol_df['close'], timeperiod=6)
symbol_df['RSI_14'] = ta.RSI(symbol_df['close'], timeperiod=14)

# ---------------------
# Apply moving averages
# ---------------------
symbol_df['SMA_20'] = ta.SMA(symbol_df['close'], timeperiod=20)
symbol_df['EMA_20'] = ta.EMA(symbol_df['close'], timeperiod=20)

# ---------------------
# Save output
# ---------------------
symbol_df.to_csv("indicator_output.csv", index=False)

print("Done! File saved: indicator_output.csv")
print(symbol_df.head())
