from src.delta_client import get_latest_candles

candles = get_latest_candles(
    symbol="BTCUSD",
    resolution="1h",
    lookback_hours=10
)

print("\n-----LATEST CANDLES-----")
print("No. of candles: ", len(candles))

for candle in candles:
    print(candle)

