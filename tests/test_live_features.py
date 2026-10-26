from src.delta_client import get_latest_candles
from src.data_loader import prepare_live_features

# Get latest candles from Delta Exchange
candles = get_latest_candles(
    symbol="BTCUSD",
    resolution="1h",
    lookback_hours=50
)

# Calculate live features
df = prepare_live_features(candles)

print("\n-----LIVE FEATURE TEST-----")

print("\nData Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.to_list())

print("\nLatest Rows:")
print(
    df[
        [
            "time",
            "close",
            "rsi",
            "cci",
            "wt1",
            "wt2",
            "plus_di",
            "minus_di",
            "adx"
        ]
    ].tail()
)

print("\nLatest Feature Vector:")
print(
    df[[
                "rsi",
                "cci",
                "wt1",
                "wt2",
                "plus_di",
                "minus_di",
                "adx"
            ]].iloc[-1]
)