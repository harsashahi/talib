import pandas as pd
import talib
import numpy as np

#  LOAD CSV 
df = pd.read_csv("daywise_ordered.csv")
df['date'] = pd.to_datetime(df['date'])

# Sort by symbol + date
df = df.sort_values(['symbol', 'date'])

#  STRATEGY FUNCTION 
def strategy(group):
    group['symbol'] = group.name  # Re-add symbol column

    o = group['open'].values
    h = group['high'].values
    l = group['low'].values
    c = group['close'].values
    v = group['volume'].values

    # Indicators
    group['RSI'] = talib.RSI(c, 14)
    group['RSI_prev'] = group['RSI'].shift(1)
    group['vol_avg_5'] = pd.Series(v).rolling(5).mean()

    # Candle directions
    group['bullish_candle'] = c > o
    group['bearish_candle'] = c < o

    # Multi-candle patterns
    group['engulfing'] = talib.CDLENGULFING(o,h,l,c)
    group['morning_star'] = talib.CDLMORNINGSTAR(o,h,l,c)
    group['evening_star'] = talib.CDLEVENINGSTAR(o,h,l,c)
    group['hammer'] = talib.CDLHAMMER(o,h,l,c)

    # Confirmation counts
    group['bull_confirm'] = (
        group['bullish_candle'].astype(int) +
        ((group['RSI']>40) & (group['RSI']>group['RSI_prev'])).astype(int) +
        (group['volume'] > group['vol_avg_5']).astype(int) +
        ((group['engulfing']>0) | (group['morning_star']>0) | (group['hammer']>0)).astype(int)
    )

    group['bear_confirm'] = (
        group['bearish_candle'].astype(int) +
        ((group['RSI']<60) & (group['RSI']<group['RSI_prev'])).astype(int) +
        (group['volume'] > group['vol_avg_5']).astype(int) +
        ((group['engulfing']<0) | (group['evening_star']<0)).astype(int)
    )

    # Signal strength
    group['signal_strength'] = np.where(
        group['bull_confirm'] >= 3, 'Strong Bullish',
        np.where(group['bull_confirm'] == 2, 'Moderate Bullish',
        np.where(group['bear_confirm'] >= 3, 'Strong Bearish',
        np.where(group['bear_confirm'] == 2, 'Moderate Bearish', 'Neutral')))
    )

    # Action
    group['action'] = np.where(
        group['signal_strength'].str.contains('Bullish'), 'BUY',
        np.where(group['signal_strength'].str.contains('Bearish'), 'SELL', 'HOLD')
    )

    return group

#  APPLY STRATEGY 
df = df.groupby('symbol', group_keys=False).apply(strategy, include_groups=False)

#  SAVE ALL HISTORICAL SIGNALS 
final_df = df[
    ['date','symbol','open','high','low','close','volume','RSI','signal_strength','action']
]
final_df.to_csv("final_confirmed_signals.csv", index=False)
print("✅ All historical signals saved: final_confirmed_signals.csv")

#  BACKTESTING 
df['future_close_3'] = df.groupby('symbol')['close'].shift(-3)
df['return_3d_pct'] = (df['future_close_3'] - df['close']) / df['close'] * 100

backtest_buy = df[df['signal_strength']=='Strong Bullish']
total_trades = len(backtest_buy)
win_rate = (backtest_buy['return_3d_pct']>0).mean()*100
avg_return = backtest_buy['return_3d_pct'].mean()
max_return = backtest_buy['return_3d_pct'].max()
min_return = backtest_buy['return_3d_pct'].min()

# Save backtesting summary to CSV
backtest_summary = pd.DataFrame({
    'Total Trades':[total_trades],
    'Win Rate (%)':[win_rate],
    'Average Return (%)':[avg_return],
    'Max Return (%)':[max_return],
    'Min Return (%)':[min_return]
})
backtest_summary.to_csv("backtesting_summary.csv", index=False)
print("✅ Backtesting summary saved: backtesting_summary.csv")

#  LATEST DAY STRONG BUY 
latest_day_df = df.groupby('symbol', group_keys=False).tail(1)
strong_buy_df = latest_day_df[latest_day_df['signal_strength']=='Strong Bullish']

strong_buy_df = strong_buy_df[
    ['date','symbol','open','high','low','close','volume','RSI','signal_strength','action']
]

strong_buy_df.to_csv("latest_strong_buy_signals.csv", index=False)
print(f"✅ {len(strong_buy_df)} Strong BUY signals exported for latest day: latest_strong_buy_signals.csv")
