import pandas as pd

from src.delta_client import get_latest_candles
from src.data_loader import (
    prepare_live_features,
    calculate_label,
    calculate_rsi,
    calculate_cci,
    calculate_wavetrend,
    calculate_adx
)
from src.lorentzian_classifier import (
    find_nearest_neighbour,
    predict_from_neighbors
)

#-------------------------------------------#
#       Configuration                       #
#-------------------------------------------#

SYMBOL = "BTCUSD"
RESOLUTION = "1h"
LOOKBACK_HOURS = 50
K = 8

FEATURE_COLUMNS = [
    "rsi",
    "cci",
    "wt1",
    "wt2",
    "plus_di",
    "minus_di",
    "adx"
]

#-------------------------------------------#
#  1. Get latest live candles.              #
#-------------------------------------------#

candles = get_latest_candles(
    symbol=SYMBOL,
    resolution=RESOLUTION,
    lookback_hours=LOOKBACK_HOURS
)

live_df = prepare_live_features(candles)

#-------------------------------------------#
#  2. Get latest feature vector.            #
#-------------------------------------------#

latest_row = live_df.iloc[-1]

current_vector = latest_row[FEATURE_COLUMNS].values

print("\n-----LIVE LORENTZIAN PREDICTION-----")

print("\nLatest Candle:")
print(latest_row["time"])

print("\nLatest feature Vector:")
print(latest_row[FEATURE_COLUMNS])

#-------------------------------------------#
#  3. Load historical dataset.              #
#-------------------------------------------#

historical_df = pd.read_csv("data/raw/BTCUSD_1h.csv")

#-------------------------------------------#
#  4. Calculate historical features.       #
#-------------------------------------------#

historical_df = calculate_rsi(historical_df)
historical_df = calculate_cci(historical_df)
historical_df = calculate_wavetrend(historical_df)
historical_df = calculate_adx(historical_df)

#-------------------------------------------#
#  5. Generate historical labels.           #
#-------------------------------------------#

historical_df = calculate_label(
    historical_df,
    horizon=4
)
#-------------------------------------------#
#  6. Remove rows with unavailable values.  #
#-------------------------------------------#

historical_df = historical_df.dropna(
    subset = FEATURE_COLUMNS + ["label"]
).reset_index(drop=True)

#-------------------------------------------#
#  7. Load historical feature matrix.       #
#-------------------------------------------#

historical_vectors = historical_df[
    FEATURE_COLUMNS
].values

#-------------------------------------------#
#  8. Find nearest neighbours.              #
#-------------------------------------------#

neighbors = find_nearest_neighbour(
    current_vector=current_vector,
    historical_vectors=historical_vectors,
    k=K
)

print("\nNearest Neighbours:")

for index, distance in neighbors:
    print(
        f"Index: {index}, "
        f"Distance: {distance:.6f}"
    )

#-------------------------------------------#
#  9. Extract neighbour indices.            #
#-------------------------------------------#

neighbor_indices = [
    index
    for index, distance in neighbors
]

#-------------------------------------------#
#  10. Generate Live Prediction.            #
#-------------------------------------------#

prediction = predict_from_neighbors(
    neighbor_indices,
    historical_df["label"]
)

#-------------------------------------------#
#  11. Display prediction.                  #
#-------------------------------------------#

print("\n-------------------------------------")
print(f"LIVE PREDICTION: {prediction}")
print("\n-------------------------------------")

if prediction == 1:
    print("Signal: LONG / BULLISH")
else:
    print("Signal: SHORT / BEARISH")