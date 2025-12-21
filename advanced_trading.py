# ADVANCED TRADER 
# Optimized for professional trading with all essential indicators

import pandas as pd
import talib 
import numpy as np 

print("ADVANCED TRADER - FILTERED COLUMNS")

# Load your complete analysis file
df = pd.read_csv('stock_analysis_COMPREHENSIVE.csv')  # Change to your actual filename

print(f"\nOriginal columns: {len(df.columns)}")
print(f"Original data: {len(df)} rows")

# ADVANCED TRADER ESSENTIALS

advanced_trader_columns = [
    # === BASIC DATA ===
    'date',
    'symbol',
    'close',
    'volume',
    
    # === TREND ANALYSIS ===
    'SMA_20',          # Short-term trend
    'SMA_50',          # Medium-term trend
    'SMA_200',         # Long-term trend (institutional level)
    
    # === MOMENTUM INDICATORS ===
    'RSI',             # Overbought/oversold
    'MACD',            # Trend momentum
    'MACD_Signal',     # MACD trigger
    'Stoch_K',         # Stochastic momentum
    
    # === VOLATILITY & RISK ===
    'BB_Upper',        # Upper Bollinger Band
    'BB_Lower',        # Lower Bollinger Band
    'ATR',             # Average True Range (for stop-loss)
    
    # === VOLUME ANALYSIS ===
    'OBV',             # On Balance Volume (money flow)
    
    # === TRADING SIGNAL ===
    'Signal',          # Buy/Sell/Hold recommendation
]

df_advanced = df[advanced_trader_columns]

# Round to 2 decimal places (keep volume as-is)
numeric_cols = df_advanced.select_dtypes(include=['float64']).columns
df_advanced[numeric_cols] = df_advanced[numeric_cols].round(2)

print("\n ADVANCED TRADER CONFIGURATION")
print(f"Total columns: {len(advanced_trader_columns)}")
print(f"\nColumns included:")
for i, col in enumerate(advanced_trader_columns, 1):
    print(f"  {i:2d}. {col}")

print("\n Sample Data (Last 5 rows):")
print(df_advanced.tail(5).to_string(index=False))

# Save the filtered file
df_advanced.to_csv('stock_analysis_ADVANCED_TRADER.csv', index=False)
print("\n Saved: stock_analysis_ADVANCED_TRADER.csv")

# WHAT EACH COLUMN IS USED FOR (ADVANCED TRADING)
print("ADVANCED TRADING - COLUMN USAGE GUIDE")

usage_guide = """
BASIC DATA (4 columns):
-----------------------
date             → Timestamp for analysis
symbol           → Stock identifier
close            → Primary price for calculations
volume           → Confirms price movements (volume = conviction)

TREND ANALYSIS (5 columns):
---------------------------
SMA_20           → Immediate trend (daily/swing trading)
                   • Price > SMA_20 = Short-term uptrend
                   • Used for quick entry/exit

SMA_50           → Swing trend (position trading)
                   • Golden Cross: SMA_20 crosses above SMA_50 = BULLISH
                   • Death Cross: SMA_20 crosses below SMA_50 = BEARISH

SMA_200          → Major trend (institutional support/resistance)
                   • Bull Market: Price > SMA_200
                   • Bear Market: Price < SMA_200

EMA_12/EMA_26    → Fast-reacting averages
                   • Used to understand MACD components
                   • EMA_12 > EMA_26 = Bullish momentum

MOMENTUM (5 columns):
---------------------
RSI              → Momentum strength (0-100)
                   • < 30 = Oversold (potential reversal up)
                   • > 70 = Overbought (potential reversal down)
                   • 40-60 = Trending market (ignore overbought/oversold)

MACD             → Trend momentum indicator
                   • MACD > 0 = Bullish pressure
                   • MACD < 0 = Bearish pressure

MACD_Signal      → MACD trigger line
                   • MACD crosses above Signal = BUY signal
                   • MACD crosses below Signal = SELL signal

MACD_Hist        → Momentum strength
                   • Positive & growing = Strong bullish momentum
                   • Negative & growing = Strong bearish momentum
                   • Converging to zero = Momentum weakening

Stoch_K          → Short-term momentum
                   • < 20 = Oversold
                   • > 80 = Overbought
                   • Use with Stoch_D for crossover signals

VOLATILITY & RISK (3 columns):
-------------------------------
BB_Upper         → Upper price boundary
                   • Price touching = Potential resistance
                   • Breakout above = Strong bullish move

BB_Lower         → Lower price boundary
                   • Price touching = Potential support
                   • Breakdown below = Strong bearish move

ATR              → Average price movement per day
                   • CRITICAL for risk management
                   • Stop-loss: Entry price ± (2 × ATR)
                   • Position size: Risk amount / ATR
                   • Higher ATR = More volatile = Smaller position

VOLUME (1 column):
------------------
OBV              → Money flow indicator
                   • Rising OBV + Rising price = Healthy uptrend
                   • Falling OBV + Rising price = Weak rally (divergence)
                   • Rising OBV + Falling price = Accumulation (potential reversal)

SIGNAL (1 column):
------------------
Signal           → Multi-indicator recommendation
                   • STRONG BUY = Multiple bullish confirmations
                   • BUY = More bullish than bearish
                   • HOLD = Wait for better setup
                   • SELL = More bearish than bullish
                   • STRONG SELL = Multiple bearish confirmations
"""

print(usage_guide)

# ADVANCED TRADING STRATEGIES

print("ADVANCED TRADING STRATEGIES WITH THESE INDICATORS")

strategies = """
STRATEGY 1: TREND FOLLOWING
---------------------------
Entry Conditions:
✓ Price > SMA_20 > SMA_50 > SMA_200 (all aligned)
✓ MACD > MACD_Signal (momentum confirmation)
✓ OBV rising (volume confirmation)
✓ RSI between 40-70 (not overbought)

Exit: When MACD crosses below Signal OR price < SMA_20


STRATEGY 2: MEAN REVERSION
---------------------------
Entry Conditions:
✓ RSI < 30 (oversold)
✓ Price touches BB_Lower (at support)
✓ Stoch_K < 20 (oversold confirmation)
✓ OBV not falling (no panic selling)

Exit: When RSI > 50 OR price reaches BB_Upper


STRATEGY 3: BREAKOUT TRADING
-----------------------------
Entry Conditions:
✓ Price breaks above BB_Upper (volatility expansion)
✓ Volume > 1.5× average (confirmation)
✓ MACD_Hist increasing (momentum building)
✓ ATR rising (volatility increasing)

Exit: When MACD_Hist starts decreasing OR ATR peaks


STRATEGY 4: DIVERGENCE TRADING
-------------------------------
Bullish Divergence:
✓ Price making lower lows
✓ RSI making higher lows (momentum improving)
✓ OBV rising (accumulation)

Bearish Divergence:
✓ Price making higher highs
✓ RSI making lower highs (momentum weakening)
✓ OBV falling (distribution)


STRATEGY 5: MULTI-TIMEFRAME CONFIRMATION
-----------------------------------------
Daily Chart:
✓ Price > SMA_200 (bull market)
✓ MACD > Signal (daily momentum up)

4-Hour Chart:
✓ Price pulls back to SMA_20 (entry point)
✓ RSI between 40-50 (dip in uptrend)

1-Hour Chart:
✓ MACD crosses above Signal (timing entry)
✓ Volume spike (confirmation)
"""

print(strategies)

# RISK MANAGEMENT WITH THESE INDICATORS
print("RISK MANAGEMENT - HOW TO USE ATR")

risk_management = """
ATR-BASED POSITION SIZING:
--------------------------

Example: You have $10,000 and risk 2% per trade = $200 risk

Stock price: $100
ATR: $2.50

Step 1: Calculate stop-loss distance
Stop-loss = 2 × ATR = 2 × $2.50 = $5.00

Step 2: Calculate position size
Position size = Risk amount / Stop-loss distance
Position size = $200 / $5.00 = 40 shares

Step 3: Execute trade
Buy: 40 shares @ $100 = $4,000
Stop-loss: $100 - $5 = $95
Maximum loss: 40 shares × $5 = $200 ✓

This way you ALWAYS risk exactly 2% regardless of volatility!


DYNAMIC STOP-LOSS LEVELS:
-------------------------
Tight stop (day trading):  Entry ± (1.0 × ATR)
Normal stop (swing):       Entry ± (2.0 × ATR)
Wide stop (position):      Entry ± (3.0 × ATR)

Higher ATR = More volatile = Use wider stops or smaller positions
"""

print(risk_management)

# ADVANCED FILTERS FOR SCREENING

print("SCREENING FILTERS - FIND BEST SETUPS")

# Create some useful filters
print("\n Finding Strong Uptrends:")
uptrend = df_advanced[
    (df_advanced['close'] > df_advanced['SMA_20']) &
    (df_advanced['SMA_20'] > df_advanced['SMA_50']) &
    (df_advanced['SMA_50'] > df_advanced['SMA_200']) &
    (df_advanced['MACD'] > df_advanced['MACD_Signal']) &
    (df_advanced['RSI'] < 70)
].tail(10)

if len(uptrend) > 0:
    print(f"Found {len(uptrend)} strong uptrend signals in last 10 days")
    print(uptrend[['date', 'close', 'RSI', 'Signal']].to_string(index=False))
else:
    print("No strong uptrend signals found recently")

print("\n Finding Oversold Opportunities:")
oversold = df_advanced[
    (df_advanced['RSI'] < 30) &
    (df_advanced['Stoch_K'] < 20) &
    (df_advanced['close'] <= df_advanced['BB_Lower'])
].tail(10)

if len(oversold) > 0:
    print(f"Found {len(oversold)} oversold signals in last 10 days")
    print(oversold[['date', 'close', 'RSI', 'Stoch_K']].to_string(index=False))
else:
    print("No oversold signals found recently")

print("\n Finding High Volatility (Trading Opportunities):")
high_vol = df_advanced.nlargest(10, 'ATR')
print(f"\nTop 10 highest ATR days (best for day trading):")
print(high_vol[['date', 'close', 'ATR', 'volume']].to_string(index=False))

# PERFORMANCE ANALYSIS

print("CURRENT MARKET ANALYSIS")

latest = df_advanced.iloc[-1]

print(f"\n Latest Data ({latest['date']}):")
print(f"  Symbol: {latest['symbol']}")
print(f"  Close: ${latest['close']:.2f}")
print(f"  Volume: {latest['volume']:,.0f}")

print(f"\n Trend Analysis:")
print(f"  SMA_20:  ${latest['SMA_20']:.2f}")
print(f"  SMA_50:  ${latest['SMA_50']:.2f}")
print(f"  SMA_200: ${latest['SMA_200']:.2f}")

trend_status = "UPTREND" if latest['close'] > latest['SMA_20'] > latest['SMA_50'] else \
               "DOWNTREND" if latest['close'] < latest['SMA_20'] < latest['SMA_50'] else \
               "SIDEWAYS"
print(f"  Status: {trend_status}")

print(f"\n Momentum:")
print(f"  RSI: {latest['RSI']:.2f}")
print(f"  MACD: {latest['MACD']:.2f}")
print(f"  Signal: {latest['MACD_Signal']:.2f}")

momentum_status = "BULLISH" if latest['MACD'] > latest['MACD_Signal'] else "BEARISH"
print(f"  Status: {momentum_status}")

print(f"\n  Risk Metrics:")
print(f"  ATR: ${latest['ATR']:.2f}")
print(f"  ATR %: {(latest['ATR'] / latest['close'] * 100):.2f}%")
print(f"  BB Range: ${latest['BB_Lower']:.2f} - ${latest['BB_Upper']:.2f}")

print(f"\n Trading Signal: {latest['Signal']}")

# Recommended action
print(f"\n Recommended Stop-Loss:")
print(f"  Long position: ${latest['close'] - (2 * latest['ATR']):.2f}")
print(f"  Short position: ${latest['close'] + (2 * latest['ATR']):.2f}")

# SUMMARY
print(" ADVANCED TRADER FILE CREATED")

summary = f"""
File: stock_analysis_ADVANCED_TRADER.csv
Columns: {len(advanced_trader_columns)}
All values rounded to 2 decimal places

This file contains EVERYTHING needed for professional trading:
✓ Trend indicators (3 SMAs + 2 EMAs)
✓ Momentum indicators (RSI, MACD, Stochastic)
✓ Volatility indicators (Bollinger Bands, ATR)
✓ Volume indicator (OBV)
✓ Trading signals

Perfect for:
• Swing trading
• Day trading
• Position trading
• Risk management
• Strategy development
"""

print(summary)

print("\n🎯 Next Steps:")
print("  1. Open stock_analysis_ADVANCED_TRADER.csv")
print("  2. Use the screening filters above to find setups")
print("  3. Apply risk management using ATR")
print("  4. Backtest your strategies")
print("  5. Combine with chart analysis")
