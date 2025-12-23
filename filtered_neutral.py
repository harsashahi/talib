import pandas as pd
import ast  # To safely convert string lists to actual lists

# Load CSV
df = pd.read_csv("latest_day_candles_names_only.csv")  # replace with your file

#  Define Bullish/Bearish Candles
bullish = [
    'CDLMORNINGSTAR','CDLMORNINGDOJISTAR','CDLHAMMER',
    'CDLINVERTEDHAMMER','CDLPIERCING','CDL3WHITESOLDIERS','CDLUNIQUE3RIVER',
    'CDLCLOSINGMARUBOZU','CDLBELTHOLD','CDLLONGLINE','CDLMARUBOZU'
]

bearish = [
    'CDLEVENINGSTAR','CDLEVENINGDOJISTAR','CDLSHOOTINGSTAR',
    'CDL3BLACKCROWS','CDLDARKCLOUDCOVER','CDL3INSIDE','CDLUPSIDEGAP2CROWS',
    'CDLSHORTLINE','CDLHIKKAKE'
]

#  Function to flag Bullish/Bearish/Neutral
def flag_signal(candle_list_str):
    try:
        candles = ast.literal_eval(candle_list_str)
        candles = [c.upper() for c in candles]
    except:
        candles = []
    if any(c in bullish for c in candles):
        return 'Bullish'
    elif any(c in bearish for c in candles):
        return 'Bearish'
    else:
        return 'Neutral'

df['Signal'] = df['Candles_Present'].apply(flag_signal)

# Count bullish and bearish candles
def count_signals(candle_list_str):
    try:
        candles = ast.literal_eval(candle_list_str)
        candles = [c.upper() for c in candles]
    except:
        candles = []
    bull_count = sum(c in bullish for c in candles)
    bear_count = sum(c in bearish for c in candles)
    return pd.Series([bull_count, bear_count])

df[['Bullish_Count','Bearish_Count']] = df['Candles_Present'].apply(count_signals)

# Signal Strength
df['Signal_Strength'] = df['Bullish_Count'] - df['Bearish_Count']

# Optional - Keep only actionable symbols
df_actionable = df[df['Signal'] != 'Neutral']

#  Save to CSV
df_actionable.to_csv("latest_day_candles_signals_filtered.csv", index=False)

#  Print summary
print("All symbols with signals:")
print(df_actionable[['symbol','Candles_Present','Signal','Bullish_Count','Bearish_Count','Signal_Strength']])
