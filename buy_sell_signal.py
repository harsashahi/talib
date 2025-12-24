import pandas as pd
import talib
import numpy as np

# Load data
df = pd.read_csv("daywise_ordered.csv")
df['date'] = pd.to_datetime(df['date'])

# Sort properly
df = df.sort_values(['symbol', 'date'])

def add_signals(group):
    close = group['close'].values
    open_ = group['open'].values
    volume = group['volume'].values

    # ===== Indicators =====
    group['RSI'] = talib.RSI(close, timeperiod=14)
    group['vol_avg_5'] = pd.Series(volume).rolling(5).mean()

    # ===== Candle Direction =====
    group['bullish_candle'] = close > open_
    group['bearish_candle'] = close < open_

    # ===== RSI Direction =====
    group['RSI_prev'] = group['RSI'].shift(1)

    # ===== Signal Logic =====
    group['signal'] = np.where(
        (group['bullish_candle']) &
        (group['RSI'] > 40) &
        (group['RSI'] > group['RSI_prev']) &
        (group['volume'] > group['vol_avg_5']),
        'BUY',
        np.where(
            (group['bearish_candle']) &
            (group['RSI'] < 60) &
            (group['RSI'] < group['RSI_prev']) &
            (group['volume'] > group['vol_avg_5']),
            'SELL',
            'HOLD'
        )
    )

    return group

# Apply per symbol
df = df.groupby('symbol', group_keys=False).apply(add_signals)

# Keep only useful columns
final_df = df[
    ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'RSI', 'signal']
]

# Save result
final_df.to_csv("buy_sell_signals.csv", index=False)

print("BUY / SELL signal file created successfully!")
