import pandas as pd

df = pd.read_csv('livedata_daywiselivedata2024.csv')

# Count unique dates
unique_dates = df['date'].nunique()

print(f"Total rows: {len(df)}")
print(f"Unique dates: {unique_dates}")
print(f"Duplicate dates per day: {len(df) / unique_dates:.1f}")

# See the date range
df['date'] = pd.to_datetime(df['date'])
print(f"\nFirst date: {df['date'].min()}")
print(f"Last date: {df['date'].max()}")
print(f"Days covered: {(df['date'].max() - df['date'].min()).days}")

# Check for duplicates
duplicates = df['date'].value_counts()
if (duplicates > 1).any():
    print(f"\n⚠️ Found duplicate dates:")
    print(duplicates[duplicates > 1].head())
    
print(df['symbol'].unique())