import pandas as pd

# Load CSV with latest day per symbol
df = pd.read_csv("latest_day_candles.csv")

# Detect all candlestick columns (assumes they start with "CDL")
candle_cols = [col for col in df.columns if col.startswith("CDL")]

# Prepare a list to store processed rows
processed_rows = []

# Process each symbol separately
for idx, row in df.iterrows():
    # Keep only candle columns that are non-zero
    non_zero_candles = [col for col in candle_cols if row[col] != 0]
    
    # Create a dict with symbol info + only non-zero candles
    new_row = row[['symbol', 'date', 'open', 'high', 'low', 'close']].to_dict()
    for col in non_zero_candles:
        new_row[col] = row[col]
    
    processed_rows.append(new_row)

# Create new DataFrame
filtered_df = pd.DataFrame(processed_rows)

# Save to CSV
filtered_df.to_csv("latest_day_nonzero_candles.csv", index=False)

print("Filtered: each symbol keeps only candle columns with non-zero values.")
