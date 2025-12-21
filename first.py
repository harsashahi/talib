import pandas as pd 
import talib 
import numpy as np

open = pd.Series([2613.7])
close = pd.Series([2618.0])
high = pd.Series([2620.0])
#low = pd.Series([2608.0])

print(talib.AROON(open, high, close))


# Example data (close prices)
#close = np.random.random(100)

# Moving averages
#sma = talib.SMA(close, timeperiod=20)
#ema = talib.EMA(close, timeperiod=20)

# RSI
#rsi = talib.RSI(close, timeperiod=14)

# MACD
#macd, signal, hist = talib.MACD(close)

# Bollinger Bands
#upper, middle, lower = talib.BBANDS(close)

#print(f"Latest RSI: {rsi[-1]}")