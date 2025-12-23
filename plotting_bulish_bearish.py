import pandas as pd
import mplfinance as mpf
import ast

# Load CSV
df = pd.read_csv("latest_day_candles_names_only.csv")  # your latest-day CSV

# Parse candles
def parse_candles(candle_list_str):
    try:
        return [c.upper() for c in ast.literal_eval(candle_list_str)]
    except:
        return []

df['Candles_Present_List'] = df['Candles_Present'].apply(parse_candles)

# Define bullish/bearish candles
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

# Flag bullish/bearish signals
def get_signal(candles):
    if any(c in bullish for c in candles):
        return 'Bullish'
    elif any(c in bearish for c in candles):
        return 'Bearish'
    else:
        return 'Neutral'

df['Signal'] = df['Candles_Present_List'].apply(get_signal)

# Plot candlestick chart for each symbol with Bullish/Bearish candles
symbols_to_plot = df[df['Signal'] != 'Neutral']['symbol'].unique()

for symbol in symbols_to_plot:
    # Filter symbol data
    symbol_df = df[df['symbol'] == symbol].copy()
    symbol_df['Date'] = pd.to_datetime(symbol_df['date'])
    symbol_df.set_index('Date', inplace=True)
    
    # Prepare OHLC dataframe
    ohlc = symbol_df[['open','high','low','close']]
    
    # Add color for Bullish/Bearish
    mc = mpf.make_marketcolors(up='green', down='red', wick='black', edge='black')
    s  = mpf.make_mpf_style(marketcolors=mc)
    
    title = f"{symbol} Candlestick Chart - Signal: {symbol_df['Signal'].iloc[0]}"
    
    mpf.plot(
        ohlc,
        type='candle',
        style=s,
        title=title,
        volume=False,
        warn_too_much_data=1000
    )
