import pandas as pd
import numpy as np

from parsers.image_parser import parse_image


import pandas as pd
import numpy as np
from parsers.image_parser import parse_image


def standardize_data(file):

    filename = file.name.lower()

    # ---------------- IMAGE ----------------
    if filename.endswith((".jpg", ".jpeg", ".png")):
        return parse_image(file)

    # ---------------- CSV ----------------
    if filename.endswith(".csv"):
        df = pd.read_csv(file)

    # ---------------- EXCEL ----------------
    elif filename.endswith((".xlsx", ".xls")):

        raw = pd.read_excel(file, header=None)

        # Your template data starts around row 3
        raw = raw.iloc[3:].reset_index(drop=True)

        df = pd.DataFrame()

        # Column positions based on template layout
        df["Date"] = raw.iloc[:, 1]

        df["BB"] = raw.iloc[:, 2]
        df["AB"] = raw.iloc[:, 3]

        df["BL"] = raw.iloc[:, 4]
        df["AL"] = raw.iloc[:, 5]

        df["BD"] = raw.iloc[:, 6]
        df["AD"] = raw.iloc[:, 7]

    else:
        raise ValueError("Unsupported file format")

    # ---------------- CLEAN DATA ----------------

    df = df.dropna(subset=["Date"])

    for col in ["BB", "AB", "BL", "AL", "BD", "AD"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert zeros to NaN (0 is usually missing reading)
    df.replace(0, np.nan, inplace=True)

    df = df.reset_index(drop=True)

    return df

    # ------------------------------------------------
    # Normalize column names
    # ------------------------------------------------
    df.columns = [str(c).lower() for c in df.columns]

    column_map = {}

    for col in df.columns:

        if "date" in col:
            column_map[col] = "Date"

        elif "pre" in col and "breakfast" in col:
            column_map[col] = "BB"

        elif "post" in col and "breakfast" in col:
            column_map[col] = "AB"

        elif "pre" in col and "lunch" in col:
            column_map[col] = "BL"

        elif "post" in col and "lunch" in col:
            column_map[col] = "AL"

        elif "pre" in col and "dinner" in col:
            column_map[col] = "BD"

        elif "post" in col and "dinner" in col:
            column_map[col] = "AD"

    df.rename(columns=column_map, inplace=True)

    # ------------------------------------------------
    # Keep required columns
    # ------------------------------------------------
    expected_cols = ["Date", "BB", "AB", "BL", "AL", "BD", "AD"]

    df = df[[c for c in expected_cols if c in df.columns]]

    # ------------------------------------------------
    # Remove empty rows
    # ------------------------------------------------
    if "Date" in df.columns:
        df = df.dropna(subset=["Date"])

    # ------------------------------------------------
    # Convert numeric columns
    # ------------------------------------------------
    for col in ["BB", "AB", "BL", "AL", "BD", "AD"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Replace zeros with NaN
    df.replace(0, np.nan, inplace=True)

    df = df.reset_index(drop=True)

    return df