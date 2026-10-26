import pandas as pd

from src.data_loader import calculate_rsi, calculate_cci, calculate_wavetrend, calculate_adx, calculate_label
from src.lorentzian_classifier import(lorentzian_distance, find_nearest_neighbour, predict_from_neighbors)


df = pd.read_csv("data/raw/BTCUSD_1h.csv")

df["time"] = pd.to_datetime(df["time"])

df = calculate_rsi(df)
df = calculate_cci(df)
df = calculate_wavetrend(df)
df = calculate_adx(df)
df = calculate_label(df, horizon=4)

# print(df[["time", "close", "rsi", "cci", "wt1", "wt2", "plus_di", "minus_di", "adx"]].to_string(index=False))

# Creating feature matrix.
features = df[
    [
        "rsi",
        "cci",
        "wt1",
        "wt2",
        "plus_di",
        "minus_di",
        "adx"
    ]
].copy()

x = [1.0, 2.0, 3.0]
y = [2.0, 3.0, 4.0]

# Remove rows containing NaN feature values
valid_features = features.dropna()

# Keep the original dataframe indices
feature_indices = valid_features.index

# Current feature vector
current_vector = valid_features.iloc[-1].values

# Historical feature vector
historical_vectors = valid_features.iloc[:-1].values

# Find nearest neighbors
neighbors = find_nearest_neighbour(
    current_vector,
    historical_vectors,
    k=8
)

print("\n---Nearest Neighbors---")

for position, distance in neighbors:

    original_index = feature_indices[position]

    print(
        f"Index: {original_index},"
        f"Distance: {distance:.6f}"
    )


distance = lorentzian_distance(x, y)
print("\nLorentzian_distance", distance)

print("\n---Neighbor Labels---")
for position, distance in neighbors:
    original_index = feature_indices[position]

    print(
        f"Index: {original_index},"
        f"Distance: {distance:.6f},"
        f"Label: {df.loc[original_index, 'label']}"
    )

neighbor_indices = [
    feature_indices[position]
    for position, distance in neighbors
]

prediction = predict_from_neighbors(
    neighbor_indices,
    df["label"]
)

print("\n---Classification Prediction---")
print("Prediction:", prediction)