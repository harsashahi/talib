import pandas as pd

# Load CSV with latest day per symbol
df = pd.read_csv("latest_day_candles.csv")

# Detect all candlestick columns (assumes they start with "CDL")
candle_cols = [col for col in df.columns if col.startswith("CDL")]

# Create a new column with names of candles that have non-zero values
df['Candles_Present'] = df[candle_cols].apply(lambda row: [col for col in candle_cols if row[col] != 0], axis=1)

# Keep only main info + the new column
df_final = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'Candles_Present']]

# Save to CSV
df_final.to_csv("latest_day_candles_names_only.csv", index=False)

print("Done! Each symbol now has a list of candlestick pattern names that are non-zero.")
