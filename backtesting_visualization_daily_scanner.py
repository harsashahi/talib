import pandas as pd
import talib
import numpy as np
import mplfinance as mpf

#  LOAD CSV 
df = pd.read_csv("daywise_ordered.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['symbol', 'date'])

#  STRATEGY FUNCTION 
def strategy(group):
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

    group['engulfing'] = talib.CDLENGULFING(o,h,l,c)
    group['morning_star'] = talib.CDLMORNINGSTAR(o,h,l,c)
    group['evening_star'] = talib.CDLEVENINGSTAR(o,h,l,c)
    group['hammer'] = talib.CDLHAMMER(o,h,l,c)

    group['bull_confirm'] = (
        group['bullish_candle'].astype(int) +
        ((group['RSI']>40) & (group['RSI']>group['RSI_prev'])).astype(int) +
        (group['volume']>group['vol_avg_5']).astype(int) +
        ((group['engulfing']>0)|(group['morning_star']>0)|(group['hammer']>0)).astype(int)
    )
    group['bear_confirm'] = (
        group['bearish_candle'].astype(int) +
        ((group['RSI']<60) & (group['RSI']<group['RSI_prev'])).astype(int) +
        (group['volume']>group['vol_avg_5']).astype(int) +
        ((group['engulfing']<0)|(group['evening_star']<0)).astype(int)
    )

    group['signal_strength'] = np.where(
        group['bull_confirm']>=3,'Strong Bullish',
        np.where(group['bull_confirm']==2,'Moderate Bullish',
        np.where(group['bear_confirm']>=3,'Strong Bearish',
        np.where(group['bear_confirm']==2,'Moderate Bearish','Neutral')))
    )
    group['action'] = np.where(
        group['signal_strength'].str.contains('Bullish'),'BUY',
        np.where(group['signal_strength'].str.contains('Bearish'),'SELL','HOLD')
    )
    return group

df = df.groupby('symbol', group_keys=False).apply(strategy, include_groups=False)

#  SAVE ALL HISTORICAL SIGNALS 
final_df = df[
    ['date','symbol','open','high','low','close','volume','RSI','signal_strength','action']
]
final_df.to_csv("final_confirmed_signals.csv", index=False)
print("✅ All historical signals saved: final_confirmed_signals.csv")

#  EXTENDED BACKTESTING 
for days in [3,5,10]:
    df[f'future_close_{days}'] = df.groupby('symbol')['close'].shift(-days)
    df[f'return_{days}d_pct'] = (df[f'future_close_{days}'] - df['close'])/df['close']*100

def backtest_summary(df, strength='Strong Bullish', days_list=[3,5,10]):
    summary = []
    for days in days_list:
        temp = df[df['signal_strength']==strength]
        total = len(temp)
        win_rate = (temp[f'return_{days}d_pct']>0).mean()*100
        avg_ret = temp[f'return_{days}d_pct'].mean()
        max_ret = temp[f'return_{days}d_pct'].max()
        min_ret = temp[f'return_{days}d_pct'].min()
        summary.append([strength, f'{days}-day', total, win_rate, avg_ret, max_ret, min_ret])
    return pd.DataFrame(summary, columns=['Signal','Period','Total Trades','Win Rate (%)','Avg Return (%)','Max Return (%)','Min Return (%)'])

backtest_buy_summary = backtest_summary(df, 'Strong Bullish')
backtest_sell_summary = backtest_summary(df, 'Strong Bearish')

backtest_full = pd.concat([backtest_buy_summary, backtest_sell_summary], ignore_index=True)
backtest_full.to_csv("backtesting_extended_summary.csv", index=False)
print("✅ Extended backtesting summary saved: backtesting_extended_summary.csv")

#  LATEST DAY SCANNER 
latest_day_df = df.groupby('symbol', group_keys=False).tail(1)

strong_buy_df = latest_day_df[latest_day_df['signal_strength']=='Strong Bullish']
strong_sell_df = latest_day_df[latest_day_df['signal_strength']=='Strong Bearish']

strong_buy_df.to_csv("latest_strong_buy_signals.csv", index=False)
strong_sell_df.to_csv("latest_strong_sell_signals.csv", index=False)
print(f"✅ Latest Strong BUY/SELL signals exported for latest day")

#  VISUALIZATION 
# Example: plot first symbol
symbol_to_plot = df['symbol'].unique()[0]
plot_df = df[df['symbol']==symbol_to_plot].copy()
plot_df.set_index('date', inplace=True)

# Align BUY/SELL markers with full index using NaN for non-signal rows
buy_y = plot_df['close'].where(plot_df['action']=='BUY', np.nan)
sell_y = plot_df['close'].where(plot_df['action']=='SELL', np.nan)

apds = [
    mpf.make_addplot(buy_y, type='scatter', marker='^', markersize=100, color='green'),
    mpf.make_addplot(sell_y, type='scatter', marker='v', markersize=100, color='red')
]

mpf.plot(plot_df, type='candle', style='yahoo', addplot=apds,
         title=f'{symbol_to_plot} BUY/SELL Signals', volume=True)
