import pandas as pd

# -------- READ FILE --------
df = pd.read_csv("livedata_daywiselivedata2024.csv")

# -------- SORT BY DATE --------
# if date column has actual date format:
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by="date", ascending=True)

# -------- RESET INDEX --------
df = df.reset_index(drop=True)

# -------- SAVE CLEAN FILE --------
df.to_csv("daywise_ordered.csv", index=False)

print("Sorting done! Saved as daywise_ordered.csv")
