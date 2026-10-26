import pandas as pd
from src.lorentzian_classifier import (
    lorentzian_distance,
    find_nearest_neighbour
)
from src.lorentzian_classifier import (
    find_nearest_neighbour
)

# Test vectors
current_vector = [50, 100]

historical_vectors = [
    [51, 101],
    [55, 110],
    [49, 98],
    [70, 150],
    [52, 103]
]

# Test Lorentzian distance
distance = lorentzian_distance(
    current_vector,
    historical_vectors[0]
)

print("Lorentzian Distance:", distance)

# Test nearest neighbours
neighbors = find_nearest_neighbour(
    current_vector,
    historical_vectors,
    k=3
)

print("\nNearest Neighbours:")
for index, distance in neighbors:
    print(f"Index: {index}, Distance: {distance:.6f}")

# Load processed BTCUSD dataset

df = pd.read_csv(
    "data/processed/BTCUSD_1h_proc.csv"
)

# Feature columns
feature_columns = [
    "close",
    "high",
    "low",
    "open",
    "volume"
]

# Select a current observation
current_index = 100

current_vector = df.loc[
    current_index,
    feature_columns
].values

# Historical observations
historical_vectors = df.loc[
    :current_index - 1,
    feature_columns
].values

# Find nearest neighbours
neighbors = find_nearest_neighbour(
    current_vector,
    historical_vectors,
    k=8
)

print("\n--- BTCUSD Nearest Neighbours ---")

for index, distance in neighbors:
    print(
        f"Index: {index}, "
        f"Distance: {distance:.6f}"
    )