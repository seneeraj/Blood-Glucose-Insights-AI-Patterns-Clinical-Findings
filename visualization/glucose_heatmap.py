import pandas as pd
import plotly.express as px


def glucose_heatmap(df):

    meals = ["BB","AB","BL","AL","BD","AD"]

    heat_df = df[meals].copy()

    # Clinical zones
    def zone(value):

        if value < 70:
            return "Hypoglycemia"

        elif value <= 140:
            return "Normal"

        elif value <= 180:
            return "Borderline"

        else:
            return "Hyperglycemia"

    zone_df = heat_df.applymap(zone)

    color_map = {
        "Hypoglycemia":"#3498db",
        "Normal":"#2ecc71",
        "Borderline":"#f1c40f",
        "Hyperglycemia":"#e74c3c"
    }

    fig = px.imshow(
        heat_df,
        labels=dict(x="Meal", y="Day", color="Glucose"),
        color_continuous_scale="RdYlGn_r",
        aspect="auto"
    )

    fig.update_layout(
        title="Glucose Heatmap (Clinical Zones)",
        xaxis_title="Meal Reading",
        yaxis_title="Day"
    )

    return fig