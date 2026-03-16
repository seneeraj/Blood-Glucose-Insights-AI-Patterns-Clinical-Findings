import json

import json
import os


def load_pattern_library():

    # Get project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    pattern_path = os.path.join(project_root, "patterns", "pattern_library.json")

    with open(pattern_path, "r") as f:
        data = json.load(f)

    return data["patterns"]


def run_pattern_engine(df):

    patterns = load_pattern_library()

    detected_patterns = []

    context = {
        "BB": df["BB"].mean(),
        "AB": df["AB"].mean(),
        "BL": df["BL"].mean(),
        "AL": df["AL"].mean(),
        "BD": df["BD"].mean(),
        "AD": df["AD"].mean(),
        "daily_mean": df.attrs["daily_mean"],
        "daily_max": df.attrs["daily_max"],
        "daily_min": df.attrs["daily_min"],
        "std_glucose": df.attrs["std_glucose"]
    }

    for pattern in patterns:

        rule = pattern["rule"]

        try:

            if eval(rule, {}, context):

                detected_patterns.append({
                    "name": pattern["name"],
                    "category": pattern["category"],
                    "severity": pattern["severity"],
                    "clinical_weight": pattern["clinical_weight"],
                    "evidence": pattern["description"]
                })

        except:
            continue

    return detected_patterns