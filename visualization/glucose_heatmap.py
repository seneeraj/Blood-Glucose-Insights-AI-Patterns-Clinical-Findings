import pandas as pd
import numpy as np
import plotly.express as px


def glucose_heatmap(df):

    meals = ["BB", "AB", "BL", "AL", "BD", "AD"]

    heat_df = df[meals].copy()

    # ------------------------------------------------
    # Replace NaN for visualization
    # ------------------------------------------------
    heat_df = heat_df.fillna(0)

    # ------------------------------------------------
    # Create heatmap
    # ------------------------------------------------
    fig = px.imshow(
        heat_df,
        labels=dict(
            x="Meal Reading",
            y="Day",
            color="Glucose"
        ),
        x=meals,
        y=df["Date"].astype(str),
        color_continuous_scale=[
            [0.0, "#3498db"],   # blue
            [0.25, "#2ecc71"],  # green
            [0.5, "#f1c40f"],   # yellow
            [1.0, "#e74c3c"]    # red
        ],
        aspect="auto"
    )

    # ------------------------------------------------
    # Layout styling
    # ------------------------------------------------
    fig.update_layout(
        title="Daily Glycemic Risk Zones",
        height=450,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig
