import pandas as pd

# Load CSV
df = pd.read_csv("stock_trading_signals_master.csv")

# Convert date column to datetime (VERY IMPORTANT)
df['date'] = pd.to_datetime(df['date'])

# Sort by symbol and date
df = df.sort_values(['symbol', 'date'])

# Keep only last date per symbol
latest_df = df.groupby('symbol', as_index=False).last()

# Save result
latest_df.to_csv("latest_per_symbol.csv", index=False)

print("Filtered latest date per symbol saved successfully.")
