import numpy as np


def generate_features(df):

    # Expected columns
    required_cols = ["BB","AB","BL","AL","BD","AD"]

    # Create missing columns if not present
    for col in required_cols:
        if col not in df.columns:
            df[col] = np.nan

    # ------------------------------------------------
    # Meal spikes
    # ------------------------------------------------
    df["breakfast_spike"] = df["AB"] - df["BB"]
    df["lunch_spike"] = df["AL"] - df["BL"]
    df["dinner_spike"] = df["AD"] - df["BD"]

    # ------------------------------------------------
    # Daily statistics
    # ------------------------------------------------
    glucose_cols = ["BB","AB","BL","AL","BD","AD"]

    df["daily_mean"] = df[glucose_cols].mean(axis=1)
    df["daily_max"] = df[glucose_cols].max(axis=1)
    df["daily_min"] = df[glucose_cols].min(axis=1)

    # ------------------------------------------------
    # Dataset level metrics
    # ------------------------------------------------
    values = df[glucose_cols].values.flatten()

    values = values[~np.isnan(values)]

    if len(values) > 0:

        df.attrs["daily_mean"] = float(np.mean(values))
        df.attrs["std_glucose"] = float(np.std(values))
        df.attrs["daily_max"] = float(np.max(values))
        df.attrs["daily_min"] = float(np.min(values))

    else:

        df.attrs["daily_mean"] = 0
        df.attrs["std_glucose"] = 0
        df.attrs["daily_max"] = 0
        df.attrs["daily_min"] = 0

    return df