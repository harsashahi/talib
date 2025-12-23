import pandas as pd
import talib

# Load CSV with latest date per symbol
df = pd.read_csv("latest_per_symbol.csv")

# Make sure numeric columns are floats
for col in ['open', 'high', 'low', 'close']:
    df[col] = df[col].astype(float)

# List of all candlestick functions you want to calculate
candle_functions = {
    'CDL2CROWS': talib.CDL2CROWS,
    'CDL3BLACKCROWS': talib.CDL3BLACKCROWS,
    'CDL3INSIDE': talib.CDL3INSIDE,
    'CDL3LINESTRIKE': talib.CDL3LINESTRIKE,
    'CDL3STARSINSOUTH': talib.CDL3STARSINSOUTH,
    'CDL3WHITESOLDIERS': talib.CDL3WHITESOLDIERS,
    'CDLABANDONEDBABY': talib.CDLABANDONEDBABY,
    'CDLADVANCEBLOCK': talib.CDLADVANCEBLOCK,
    'CDLBELTHOLD': talib.CDLBELTHOLD,
    'CDLBREAKAWAY': talib.CDLBREAKAWAY,
    'CDLCLOSINGMARUBOZU': talib.CDLCLOSINGMARUBOZU,
    'CDLCONCEALBABYSWALL': talib.CDLCONCEALBABYSWALL,
    'CDLCOUNTERATTACK': talib.CDLCOUNTERATTACK,
    'CDLDARKCLOUDCOVER': talib.CDLDARKCLOUDCOVER,
    'CDLDOJI': talib.CDLDOJI,
    'CDLDOJISTAR': talib.CDLDOJISTAR,
    'CDLDRAGONFLYDOJI': talib.CDLDRAGONFLYDOJI,
    'CDLENGULFING': talib.CDLENGULFING,
    'CDLEVENINGDOJISTAR': talib.CDLEVENINGDOJISTAR,
    'CDLEVENINGSTAR': talib.CDLEVENINGSTAR,
    'CDLGAPSIDESIDEWHITE': talib.CDLGAPSIDESIDEWHITE,
    'CDLGRAVESTONEDOJI': talib.CDLGRAVESTONEDOJI,
    'CDLHAMMER': talib.CDLHAMMER,
    'CDLHANGINGMAN': talib.CDLHANGINGMAN,
    'CDLHARAMI': talib.CDLHARAMI,
    'CDLHARAMICROSS': talib.CDLHARAMICROSS,
    'CDLHIGHWAVE': talib.CDLHIGHWAVE,
    'CDLHIKKAKE': talib.CDLHIKKAKE,
    'CDLHIKKAKEMOD': talib.CDLHIKKAKEMOD,
    'CDLHOMINGPIGEON': talib.CDLHOMINGPIGEON,
    'CDLIDENTICAL3CROWS': talib.CDLIDENTICAL3CROWS,
    'CDLINNECK': talib.CDLINNECK,
    'CDLINVERTEDHAMMER': talib.CDLINVERTEDHAMMER,
    'CDLKICKING': talib.CDLKICKING,
    'CDLKICKINGBYLENGTH': talib.CDLKICKINGBYLENGTH,
    'CDLLADDERBOTTOM': talib.CDLLADDERBOTTOM,
    'CDLLONGLEGGEDDOJI': talib.CDLLONGLEGGEDDOJI,
    'CDLLONGLINE': talib.CDLLONGLINE,
    'CDLMARUBOZU': talib.CDLMARUBOZU,
    'CDLMATCHINGLOW': talib.CDLMATCHINGLOW,
    'CDLMATHOLD': talib.CDLMATHOLD,
    'CDLMORNINGDOJISTAR': talib.CDLMORNINGDOJISTAR,
    'CDLMORNINGSTAR': talib.CDLMORNINGSTAR,
    'CDLONNECK': talib.CDLONNECK,
    'CDLPIERCING': talib.CDLPIERCING,
    'CDLRICKSHAWMAN': talib.CDLRICKSHAWMAN,
    'CDLRISEFALL3METHODS': talib.CDLRISEFALL3METHODS,
    'CDLSEPARATINGLINES': talib.CDLSEPARATINGLINES,
    'CDLSHOOTINGSTAR': talib.CDLSHOOTINGSTAR,
    'CDLSHORTLINE': talib.CDLSHORTLINE,
    'CDLSPINNINGTOP': talib.CDLSPINNINGTOP,
    'CDLSTALLEDPATTERN': talib.CDLSTALLEDPATTERN,
    'CDLSTICKSANDWICH': talib.CDLSTICKSANDWICH,
    'CDLTAKURI': talib.CDLTAKURI,
    'CDLTASUKIGAP': talib.CDLTASUKIGAP,
    'CDLTHRUSTING': talib.CDLTHRUSTING,
    'CDLTRISTAR': talib.CDLTRISTAR,
    'CDLUNIQUE3RIVER': talib.CDLUNIQUE3RIVER,
    'CDLUPSIDEGAP2CROWS': talib.CDLUPSIDEGAP2CROWS,
    'CDLXSIDEGAP3METHODS': talib.CDLXSIDEGAP3METHODS
}

# Step 1: Calculate all candle signals
for name, func in candle_functions.items():
    df[name] = func(df['open'], df['high'], df['low'], df['close'])

# Step 2: Optionally keep only candles with any value
candle_cols = list(candle_functions.keys())
non_zero_candles = [col for col in candle_cols if df[col].ne(0).any()]
final_df = df[['symbol', 'date', 'open', 'high', 'low', 'close'] + non_zero_candles]

# Step 3: Save to CSV
final_df.to_csv("latest_day_candles.csv", index=False)

print(f"Calculated {len(non_zero_candles)} candlestick patterns with values")
