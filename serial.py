import pandas as pd

input_file = "daywise_ordered.csv"
output_file = "floorsheet_serial_by_symbol.csv"

df = pd.read_csv(input_file)

# normalize column names
df.columns = df.columns.str.strip().str.lower()

print("Detected columns:", df.columns.tolist())

# date column
if 'date' not in df.columns:
    raise ValueError(" 'date' column not found")

df['date'] = pd.to_datetime(df['date'])

# detect order column
order_col = None
possible_order_cols = [
    'contract_id', 'contract no', 'contract_no',
    'sn', 's.n', 'id', 'trade_id'
]

for col in df.columns:
    if col in possible_order_cols:
        order_col = col
        break

# sort correctly
if order_col:
    print(f"Using order column: {order_col}")
    df = df.sort_values(['symbol', 'date', order_col])
else:
    print(" No contract column found → using row order")
    df = df.sort_values(['symbol', 'date']).reset_index(drop=True)

# SERIAL NUMBER PER SYMBOL
df['serial_no'] = df.groupby('symbol').cumcount() + 1

# save
df.to_csv(output_file, index=False)

print(f"✅ Saved: {output_file}")
