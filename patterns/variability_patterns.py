import numpy as np
from core.pattern_registry import register_pattern

@register_pattern
def detect_high_variability(df):

    if df.empty:
        return None

    values = df[["BB","AB","BL","AL","BD","AD"]].values.flatten()

    # remove zeros or NaN
    values = [v for v in values if v is not None]

    if len(values) == 0:
        return None

    std = np.std(values)

    if std > 60:

        return {
            "name": "High Glycemic Variability",
            "category": "Variability",
            "severity": 0.8,
            "frequency": 0.7,
            "clinical_weight": 0.9,
            "evidence": f"Std deviation {round(std,1)}"
        }

    return None