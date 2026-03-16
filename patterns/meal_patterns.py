from core.pattern_registry import register_pattern


@register_pattern
def detect_breakfast_spike(df):

    spikes = df["breakfast_spike"]

    avg_spike = spikes.mean()

    frequency = (spikes > 120).mean()

    if avg_spike > 100:

        return {
            "name": "Severe Breakfast Spike",
            "category": "Meal Response",
            "severity": 0.9,
            "frequency": frequency,
            "clinical_weight": 0.9,
            "evidence": f"Average spike {round(avg_spike,1)} mg/dL"
        }


@register_pattern
def detect_lunch_spike(df):

    spikes = df["lunch_spike"]

    avg_spike = spikes.mean()

    frequency = (spikes > 100).mean()

    if avg_spike > 80:

        return {
            "name": "Lunch Spike",
            "category": "Meal Response",
            "severity": 0.7,
            "frequency": frequency,
            "clinical_weight": 0.7,
            "evidence": f"Average spike {round(avg_spike,1)} mg/dL"
        }