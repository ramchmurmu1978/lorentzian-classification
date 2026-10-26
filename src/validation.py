import pandas as pd

from src.data_loader import(
    calculate_rsi,
    calculate_cci,
    calculate_wavetrend,
    calculate_adx,
    calculate_label
)

from src.lorentzian_classifier import(
    find_nearest_neighbour,
    predict_from_neighbors
)

def generate_predictions(df, features, k=8):
    """
Generate Lorentzian Classification predictions
for valid historical observations.
    """
    valid_features = features.dropna()

    predictions = []
    actual_labels = []

    feature_indices = valid_features.index

    for current_position in range(1, len(valid_features)):
        current_vector = valid_features.iloc[current_position].values

        historical_vectors = valid_features.iloc[
            :current_position
        ].values

        neighbors = find_nearest_neighbour(
            current_vector,
            historical_vectors,
            k=min(k, len(historical_vectors))
        )

        neighbor_indices = [
            feature_indices[position]
            for position, distance in neighbors 
        ]

        prediction = predict_from_neighbors(
            neighbor_indices,
            df["label"]
        )

        actual_label = df.loc[
            feature_indices[current_position],
            "label"
        ]

        predictions.append(prediction)
        actual_labels.append(actual_label)

    return predictions, actual_labels

def validate_predictions(predictions, actual_labels):
    
    print("\n---Prediction Validation---")

# Total predictions
    print("Total Predictions:", len(predictions))

    prediction_series = pd.Series(predictions)
    actual_series = pd.Series(actual_labels)

# Remove observations where actual label is undefined (NaN)
    valid_mask = actual_series.notna()

    valid_predictions = prediction_series[valid_mask]
    valid_actuals = actual_series[valid_mask]

# NaN Distribution
    print("\nActual NaN Count: ", actual_series.isna().sum())
    print("\nPrediction NaN Count: ", prediction_series.isna().sum())

# Prediction Distribution
    print("\nPrediction Counts:")
    print(valid_predictions.value_counts())

    print("\nActual Label Counts:")
    print(valid_actuals.value_counts())

# Accuracy Calculation  
    correct = (valid_predictions == valid_actuals).sum()
    total = len(valid_actuals)
    accuracy = correct / total

    print("\nCorrect Prediction: ", correct)
    print("\nIncorrect Prediction: ", total - correct)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Accuracy (%): {accuracy * 100:.2f}%")

    print("\n----Confusion Matrix----")
    confusion_matrix = pd.crosstab(
        valid_actuals,
        valid_predictions,
        rownames=["Actual"],
        colnames=["Predicted"]
    )
    print(confusion_matrix)

    print("\n---Sample Prediction---")

    validation_df = pd.DataFrame({
        "Actual": valid_actuals,
        "Predicted": valid_predictions
    })

    print(validation_df.head(20))

if __name__ == "__main__":

    print("----Phase 4 validation----")

    df = pd.read_csv("data/raw/BTCUSD_1h.csv")

    df["time"] = pd.to_datetime(df["time"])

    df = calculate_rsi(df)
    df = calculate_cci(df)
    df = calculate_wavetrend(df)
    df = calculate_adx(df)
    df = calculate_label(df, horizon=4)

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

    predictions, actual_labels = generate_predictions(
        df,
        features,
        k=8
    )
    print("\n----Label Check----")
    print(df[["time", "close", "label"]].head(20))

    print("\n----Label Distribution----")
    print(df["label"].value_counts(dropna=False))

    validate_predictions(
        predictions,
        actual_labels
    )