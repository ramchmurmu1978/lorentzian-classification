import sys
import pandas as pd
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.delta_client import get_historical_candles

# BTC 1-hr historical data
symbol = "BTCUSD"
resolution = "1h"

start = 1757635200
end = 1761264000

# Fetch data
data = get_historical_candles (
    symbol=symbol,
    resolution=resolution,
    start=start,
    end=end
)

# Convert to DataFrame
df = pd.DataFrame(data["result"])

# Convert timestamp
df["time"] = pd.to_datetime(df["time"], unit="s")

# Sort Chronologically
df = df.sort_values("time").reset_index(drop=True)

print("\n--- Dataset Validation ---")

print("\nDataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Timestamp:")
print(df["time"].duplicated().sum())

print("\nTime Range:")
print("Start :", df["time"].min())
print("End :", df["time"].max())

print("\nChornological order:")
print(df["time"].is_monotonic_increasing)

df.to_csv("data/processed/BTCUSD_1h_proc.csv", index=False)
print("\nProcessed dataset saved successfully.")