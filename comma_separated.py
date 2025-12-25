import pandas as pd

# Load CSV
df = pd.read_csv("latest_day_candles.csv")

# Detect candle columns
candle_cols = [col for col in df.columns if col.startswith("CDL")]

# ===============================
# Step 1: Convert binary → %
# ===============================
def compute_strength_percent(row):
    total = row[candle_cols].sum()
    if total == 0:
        return row[candle_cols] * 0
    # Each detected candle gets equal %
    return row[candle_cols].apply(
        lambda x: round((100 / total), 2) if x != 0 else 0
    )

df[candle_cols] = df.apply(compute_strength_percent, axis=1)

# ===============================
# Step 2: Keep only max-strength candles
# ===============================
def get_max_candles(row):
    max_strength = row[candle_cols].max()
    candles = [
        col.replace("CDL", "")
        for col in candle_cols
        if row[col] == max_strength and max_strength > 0
    ]
    return ','.join(candles), max_strength

df[['Candles_Present', 'Max_Candle_Strength']] = df.apply(
    lambda r: pd.Series(get_max_candles(r)), axis=1
)

# ===============================
# Final columns
# ===============================
df_final = df[
    ['symbol', 'date', 'open', 'high', 'low', 'close',
     'Candles_Present', 'Max_Candle_Strength']
]

# Remove rows with no candles
df_final = df_final[df_final['Candles_Present'] != '']

# Save
df_final.to_csv(
    "latest_day_candles_strength_percent2.csv",
    index=False,
    encoding="utf-8"
)

print("✅ Done! Strength is now in PERCENT (25, 50, 100)")
