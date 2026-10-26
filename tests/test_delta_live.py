import time

from src.delta_client import get_historical_candles

# Current time in milliseconds
end = int(time.time())

# Fetch the previous 2 hours
start = end - (2 * 60 * 60)

data = get_historical_candles(
    symbol="BTCUSD",
    resolution="1h",
    start=start,
    end=end
)
print("\n------DELTA API TEST------")
print("Response type:", type(data))

print("Response:")
print(data)