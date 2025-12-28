import pandas as pd

input_file = "floorsheet_serial_by_symbol.csv"
output_file = "pvvr_output.csv"

df = pd.read_csv(input_file)

# normalize column names
df.columns = df.columns.str.strip().str.lower()

# required columns check
required = ['symbol', 'date', 'close', 'volume']
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")

# convert date
df['date'] = pd.to_datetime(df['date'])

# sort properly
df = df.sort_values(['symbol', 'date'])

# previous close
df['prev_close'] = df.groupby('symbol')['close'].shift(1)

# price change %
df['price_change_pct'] = (
    (df['close'] - df['prev_close']) / df['prev_close']
) * 100

# PVVR calculation
df['pvvr'] = df['price_change_pct'] * df['volume']

# optional rounding
df['price_change_pct'] = df['price_change_pct'].round(2)
df['pvvr'] = df['pvvr'].round(2)

# save
df.to_csv(output_file, index=False)

print("✅ PVVR file saved as:", output_file)
