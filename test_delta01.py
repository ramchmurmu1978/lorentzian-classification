import pandas as pd
from src.delta_client import get_historical_candles

data = get_historical_candles(
    symbol="BTCUSD",
    resolution="1h",
    start=1757635200,  # Example start timestamp in milliseconds
    end=1757721600     # Example end timestamp in milliseconds
)

df = pd.DataFrame(data["result"])

# Convert unix timestamp to datetime
df["time"] = pd.to_datetime(df["time"], unit="s")

# Sort oldest -> newest
df = df.sort_values("time").reset_index(drop=True)

print("\n--- Dataset Validation ---")

print("Rows: ", len(df))

print("\nMissing values: ")
print(df.isnull().sum())

print("\nDuplicate timestamps :", df["time"].duplicated().sum())

print("\nData types: ")
print(df.dtypes)

print("\nOHLC Validation:")

print("High >= Open: ",
      (df["high"] >= df["open"]).all())

print("High >= Close: ",
      (df["high"] >= df["close"]).all())

print("Low <= Open: ",
      (df["low"] <= df["open"]).all())

print("Low <= Close: ",
      (df["low"] <= df["close"]).all())

# print(df.to_string(index=False))

df.to_csv("data/processed/BTCUSD_1h_proc.csv", index=False)
print("\nData saved successfully.")