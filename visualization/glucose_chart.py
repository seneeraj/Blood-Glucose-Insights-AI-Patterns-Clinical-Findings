import plotly.graph_objects as go

def plot_glucose(df):

    fig = go.Figure()

    for col in ["BB","AB","BL","AL","BD","AD"]:

        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df[col],
                mode="lines+markers",
                name=col
            )
        )

    fig.update_layout(
        title="Daily Glucose Readings",
        xaxis_title="Date",
        yaxis_title="Glucose (mg/dL)",
        hovermode="x unified"
    )

    return fig