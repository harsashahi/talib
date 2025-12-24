import pandas as pd
import talib
import numpy as np

df = pd.read_csv("daywise_ordered.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['symbol', 'date'])

def strategy(group):
    # ✅ Re-add symbol column
    group['symbol'] = group.name

    o = group['open'].values
    h = group['high'].values
    l = group['low'].values
    c = group['close'].values
    v = group['volume'].values

    group['RSI'] = talib.RSI(c, 14)
    group['RSI_prev'] = group['RSI'].shift(1)
    group['vol_avg_5'] = pd.Series(v).rolling(5).mean()

    group['bullish_candle'] = c > o
    group['bearish_candle'] = c < o

    group['engulfing'] = talib.CDLENGULFING(o, h, l, c)
    group['morning_star'] = talib.CDLMORNINGSTAR(o, h, l, c)
    group['evening_star'] = talib.CDLEVENINGSTAR(o, h, l, c)
    group['hammer'] = talib.CDLHAMMER(o, h, l, c)

    group['bull_confirm'] = (
        group['bullish_candle'].astype(int) +
        ((group['RSI'] > 40) & (group['RSI'] > group['RSI_prev'])).astype(int) +
        (group['volume'] > group['vol_avg_5']).astype(int) +
        ((group['engulfing'] > 0) | (group['morning_star'] > 0) | (group['hammer'] > 0)).astype(int)
    )

    group['bear_confirm'] = (
        group['bearish_candle'].astype(int) +
        ((group['RSI'] < 60) & (group['RSI'] < group['RSI_prev'])).astype(int) +
        (group['volume'] > group['vol_avg_5']).astype(int) +
        ((group['engulfing'] < 0) | (group['evening_star'] < 0)).astype(int)
    )

    group['signal_strength'] = np.where(
        group['bull_confirm'] >= 3, 'Strong Bullish',
        np.where(group['bull_confirm'] == 2, 'Moderate Bullish',
        np.where(group['bear_confirm'] >= 3, 'Strong Bearish',
        np.where(group['bear_confirm'] == 2, 'Moderate Bearish', 'Neutral')))
    )

    group['action'] = np.where(
        group['signal_strength'].str.contains('Bullish'), 'BUY',
        np.where(group['signal_strength'].str.contains('Bearish'), 'SELL', 'HOLD')
    )

    return group

df = (
    df.groupby('symbol', group_keys=False)
      .apply(strategy, include_groups=False)
)

final_df = df[
    ['date','symbol','open','high','low','close','volume',
     'RSI','signal_strength','action']
]

final_df.to_csv("final_confirmed_signals.csv", index=False)

print("✅ Script executed successfully – symbol issue fixed")
