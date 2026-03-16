import plotly.graph_objects as go


def meal_response_chart(df):

    meals = ["Breakfast", "Lunch", "Dinner"]

    before = [
        df["BB"].mean(),
        df["BL"].mean(),
        df["BD"].mean()
    ]

    after = [
        df["AB"].mean(),
        df["AL"].mean(),
        df["AD"].mean()
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=meals,
            y=before,
            name="Before Meal"
        )
    )

    fig.add_trace(
        go.Bar(
            x=meals,
            y=after,
            name="After Meal"
        )
    )

    fig.update_layout(
        title="Meal Response Pattern",
        xaxis_title="Meal",
        yaxis_title="Glucose (mg/dL)",
        barmode="group"
    )

    return fig