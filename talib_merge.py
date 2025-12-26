import pandas as pd
import talib 

# FILE PATHS
STRENGTH_FILE = "your_file_cleaned2.csv"
CANDLE_FILE = "latest_day_candles_names_only3.csv"
OUTPUT_FILE = "symbol_highest_strength_candle.csv"

# OFFICIAL TA-Lib NAME MAP
TALIB_MAP = {
   
    "Morning Doji Star": "DOJISTAR",
    "Dark Cloud Cover": "DARKCLOUDCOVER",
    "Hanging Man": "HANGINGMAN",
    "Two Crow": "TWOCROWS",
    "3 Black Crows": "3BLACKCROWS",
    "3 Inside": "3INSIDE",
    "3 Line Strike": "3LINESTRIKE",
    "3 Outside": "3OUTSIDE",
    "3 Stars In South": "3STARSINSOUTH",
    "3 White Soldiers": "3WHITESOLDIERS",
    "Abandoned Baby": "ABANDONEDBABY",
    "Advance Block": "ADVANCEBLOCK",
    "Belt Hold": "BELTHOLD",
    "Breakaway": "BREAKAWAY",
    "Closing Marubozu": "CLOSINGMARUBOZU",
    "Conceal Baby Swallow": "CONCEALBABYSWALL",
    "Counterattack": "COUNTERATTACK",
    "Doji": "DOJI",
    "Doji Star": "DOJISTAR",
    "Dragonfly Doji": "DRAGONFLYDOJI",
    "Engulfing": "ENGULFING",
    "Evening Doji Star": "EVENINGDOJISTAR",
    "Evening Star": "EVENINGSTAR",
    "Gap Side-by-side White": "GAPSIDESIDEWHITE",
    "Grave Stone Doji": "GRAVESTONEDOJI",
    "Hammer": "HAMMER",
    "Harami": "HARAMI",
    "Harami Cross": "HARAMICROSS",
    "High Wave": "HIGHWAVE",
    "Hikkake": "HIKKAKE",
    "Hikkake Modified": "HIKKAKEMOD",
    "Homing Pigeon": "HOMINGPIGEON",
    "Identical 3 Crows": "IDENTICAL3CROWS",
    "In Neck": "INNECK",
    "Inside": "INSIDE",
    "Inverted Hammer": "INVERTEDHAMMER",
    "Kicking": "KICKING",
    "Kicking By Length": "KICKINGBYLENGTH",
    "Ladder Bottom": "LADDERBOTTOM",
    "Long Legged Doji": "LONGLEGGEDDOJI",
    "Longline": "LONGLINE",
    "Marubozu": "MARUBOZU",
    "Matching Low": "MATCHINGLOW",
    "Mat Hold": "MATHOLD",
    "Morning Star": "MORNINGSTAR",
    "On Neck": "ONNECK",
    "Piercing": "PIERCING",
    "Rickshaw Man": "RICKSHAWMAN",
    "Rise Fall 3 Methods": "RISEFALL3METHODS",
    "Separating Lines": "SEPARATINGLINES",
    "Shooting Star": "SHOOTINGSTAR",
    "Shortline": "SHORTLINE",
    "Spinning Top": "SPINNINGTOP",
    "Stalled Pattern": "STALLEDPATTERN",
    "Stick Sandwich": "STICKSANDWICH",
    "Takuri": "TAKURI",
    "Tasuki Gap": "TASUKIGAP",
    "Thrusting": "THRUSTING",
    "Tri-star": "TRISTAR",
    "Unique 3 River": "UNIQUE3RIVER",
    "Upside Gap 2 Crows": "UPSIDEGAP2CROWS",
    "Xside Gap 3 Methods": "XSIDEGAP3METHODS"
}
 

# LOAD DATA
strength_df = pd.read_csv(STRENGTH_FILE)
price_df = pd.read_csv(CANDLE_FILE)

# MAP STRENGTH CANDLES → TA-Lib
strength_df["talib_name"] = strength_df["candle_name"].map(TALIB_MAP)
strength_df["strength_percentage"] = pd.to_numeric(
    strength_df["strength_percentage"], errors="coerce"
)

strength_df = strength_df.dropna(subset=["talib_name"])

# CLEAN PRICE DATA
price_df["Candles_Present"] = price_df["Candles_Present"].fillna("")

expanded = price_df.assign(
    talib_name=price_df["Candles_Present"].str.split(",")
).explode("talib_name")

expanded["talib_name"] = expanded["talib_name"].str.replace("CDL", "", regex=False).str.strip()

# MERGE STRENGTH
merged = expanded.merge(
    strength_df[["talib_name", "strength_percentage"]],
    on="talib_name",
    how="left"
)

# KEEP HIGHEST STRENGTH PER SYMBOL
final_df = (
    merged.sort_values("strength_percentage", ascending=False)
    .groupby("symbol", as_index=False)
    .first()
)

# FINAL OUTPUT
final_df = final_df[
    [
        "symbol",
        "date",
        "open",
        "high",
        "low",
        "close",
        "talib_name",
        "strength_percentage",
    ]
]

final_df.rename(columns={"talib_name": "candle_name"}, inplace=True)

# SAVE CSV
final_df.to_csv(OUTPUT_FILE, index=False)
final_df.to_csv("final_talib_matched.csv", index=False)


print("✅ FIXED: Correct candle strength matched (NO MORE 0%)")
