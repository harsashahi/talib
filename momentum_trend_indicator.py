import pandas as pd
import talib
import numpy as np

# Load data
df = pd.read_csv("indicators_all_symbols.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["symbol", "date"])

# Indicator calculation
def calculate_indicators(group):
    group = group.sort_values("date")

    open_ = group["open"].values
    high  = group["high"].values
    low   = group["low"].values
    close = group["close"].values

    # ===== Trend / Momentum (TA-Lib) =====
    macd, macd_signal, _ = talib.MACD(close, 12, 26, 9)
    group["MACD"] = macd
    group["MACD_SIGNAL"] = macd_signal

    group["PPO"] = talib.PPO(close, 12, 26)
    group["TRIX"] = talib.TRIX(close, 18)
    group["WILLR"] = talib.WILLR(high, low, close, 13)

    group["PLUS_DM"] = talib.PLUS_DM(high, low, 14)
    group["MINUS_DM"] = talib.MINUS_DM(high, low, 14)

    # ===== Oscillators =====
    group["BOP"] = talib.BOP(open_, high, low, close)
    group["CCI_20"] = talib.CCI(high, low, close, 20)
    group["CMO_9"] = talib.CMO(close, 9)

    slowk, slowd = talib.STOCH(high, low, close, 14, 3, 0, 3, 0)
    group["STOCH_K"] = slowk
    group["STOCH_D"] = slowd

    stochrsi_k, stochrsi_d = talib.STOCHRSI(close, 14, 14, 3, 0)
    group["STOCHRSI_K"] = stochrsi_k
    group["STOCHRSI_D"] = stochrsi_d

    group["UO"] = talib.ULTOSC(high, low, close, 7, 14, 28)

    # ===== COPPOCK (manual) =====
    roc11 = talib.ROC(close, 11)
    roc14 = talib.ROC(close, 14)
    group["COPPOCK"] = talib.WMA(roc11 + roc14, 10)

    # ===== KST (manual) =====
    rcma1 = talib.SMA(talib.ROC(close, 10), 10)
    rcma2 = talib.SMA(talib.ROC(close, 15), 10)
    rcma3 = talib.SMA(talib.ROC(close, 20), 10)
    rcma4 = talib.SMA(talib.ROC(close, 30), 15)

    group["KST"] = rcma1 + rcma2 + rcma3 + rcma4
    group["KST_SIGNAL"] = talib.SMA(group["KST"], 5)

    return group

# Apply per symbol
df = df.groupby("symbol", group_keys=False).apply(calculate_indicators)

# Save output
df.to_csv("momentum_trend_output.csv", index=False)
print("✅ Indicators calculated successfully")
