import pandas as pd

# Load CSV
df = pd.read_csv("all_candlestick_values_full_history.csv")

# Detect all candlestick columns
candle_cols = [col for col in df.columns if col.startswith("CDL")]

# Step 1: Remove rows where all candle columns are 0
df = df[df[candle_cols].ne(0).any(axis=1)]

# Step 2: Remove symbols that no longer have any rows
# (optional if Step 1 already removed all-zero symbols)
symbols_with_candles = df['symbol'].unique()
df = df[df['symbol'].isin(symbols_with_candles)]

# Save filtered CSV
df.to_csv("filtered_symbols_and_candles.csv", index=False)

print(f"Rows after removing all-zero candles: {len(df)}")
print(f"Symbols after removing all-zero symbols: {df['symbol'].nunique()}")
