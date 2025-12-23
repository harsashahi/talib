import pandas as pd
import ast  # To safely convert string lists to actual lists

# Load CSV
df = pd.read_csv("latest_day_candles_names_only.csv")  # replace with your file

# Define bullish and bearish patterns
bullish = [
    'CDLMORNINGSTAR','CDLMORNINGDOJISTAR','CDLHAMMER',
    'CDLINVERTEDHAMMER','CDLPIERCING','CDL3WHITESOLDIERS','CDLUNIQUE3RIVER'
]

bearish = [
    'CDLEVENINGSTAR','CDLEVENINGDOJISTAR','CDLSHOOTINGSTAR',
    'CDL3BLACKCROWS','CDLDARKCLOUDCOVER','CDL3INSIDE','CDLUPSIDEGAP2CROWS'
]

# Function to flag signal
def flag_signal(candle_list_str):
    try:
        # Convert string representation of list to actual list
        candles = ast.literal_eval(candle_list_str)
        # Make all uppercase to ensure matching
        candles = [c.upper() for c in candles]
    except:
        candles = []

    if any(c in bullish for c in candles):
        return 'Bullish'
    elif any(c in bearish for c in candles):
        return 'Bearish'
    else:
        return 'Neutral'

# Apply function
df['Signal'] = df['Candles_Present'].apply(flag_signal)

# Save to new CSV
df.to_csv("latest_day_candles_with_signal.csv", index=False)

print(df[['symbol','Candles_Present','Signal']])
