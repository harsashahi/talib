import pandas as pd
import numpy as np

# Load your CSV
df = pd.read_csv("floorsheet_serial_by_symbol.csv")  # replace with your actual CSV
# df = pd.read_csv("your_data.csv")  # if CSV

# Make sure date is datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by symbol and date
df = df.sort_values(['symbol', 'date'])

# Function to calculate PVVR for each symbol
def calculate_pvvr(group, window=14):
    """
    PVVR = (Volume Volatility / Avg Volume) / (Price Volatility / Avg Price Change)
    """
    # Price volatility: standard deviation of close price
    group['price_volatility'] = group['close'].rolling(window).std()
    
    # Avg price change: mean of absolute difference between consecutive close prices
    group['avg_price_change'] = group['close'].diff().abs().rolling(window).mean()
    
    # Volume volatility: std of volume
    group['volume_volatility'] = group['volume'].rolling(window).std()
    
    # Avg volume
    group['avg_volume'] = group['volume'].rolling(window).mean()
    
    # PVVR calculation
    group['pvvr'] = (group['volume_volatility'] / group['avg_volume']) / \
                    (group['price_volatility'] / group['avg_price_change'])
    
    return group

# Apply calculation per symbol
df = df.groupby('symbol').apply(calculate_pvvr)

# Keep only relevant columns
df_result = df[['date', 'symbol', 'close', 'volume', 'pvvr']]

# Save result
df_result.to_csv("pvvr_calculated.csv", index=False)

print(df_result.tail(20))
