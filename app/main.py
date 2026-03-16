import sys
import os

# ------------------------------------------------
# Add project root to Python path
# ------------------------------------------------
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd

from core.data_standardizer import standardize_data
from core.feature_engineering import generate_features
from core.pattern_engine import run_pattern_engine
from core.pattern_scoring import rank_patterns, get_top_patterns

from visualization.glucose_chart import plot_glucose
from visualization.glucose_heatmap import glucose_heatmap
from visualization.meal_response_chart import meal_response_chart


# ------------------------------------------------
# Convert dataframe to Streamlit safe format
# ------------------------------------------------
def make_streamlit_safe(df):

    df_safe = pd.DataFrame(df.to_dict(orient="records"))

    if "Date" in df_safe.columns:
        df_safe["Date"] = df_safe["Date"].astype(str)

    return df_safe


# ------------------------------------------------
# Pattern card UI
# ------------------------------------------------
def pattern_card(rank, pattern):

    score = pattern.get("score", 0)

    if score > 0.9:
        color = "#ff4b4b"
    elif score > 0.7:
        color = "#ffa500"
    else:
        color = "#4CAF50"

    st.markdown(
        f"""
        <div style="
        border-left:6px solid {color};
        padding:10px;
        margin-bottom:8px;
        background:#fafafa;
        border-radius:6px;">
        <b>{rank}. {pattern.get('name','Pattern')}</b><br>
        Score: {score}<br>
        {pattern.get('description','')}
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------
# Page Configuration
# ------------------------------------------------
st.set_page_config(
    page_title="AI Glucose Pattern Analyzer",
    layout="wide"
)

st.title("Blood Glucose Insights AI Patterns & Clinical Findings")
st.caption("Upload glucose log → Detect hidden clinical patterns → Identify metabolic risks")


# ------------------------------------------------
# Sidebar Upload
# ------------------------------------------------
st.sidebar.header("Upload Glucose Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload file",
    type=["csv","xlsx","xls","jpg","jpeg","png"]
)

st.sidebar.caption("Supported: Excel, CSV, Image")


# ------------------------------------------------
# Main Pipeline
# ------------------------------------------------
if uploaded_file:

    try:

        # -----------------------------
        # Data extraction
        # -----------------------------
        df = standardize_data(uploaded_file)

        if df is None or df.empty:
            st.error("No glucose data detected")
            st.stop()

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])

        # -----------------------------
        # Feature Engineering
        # -----------------------------
        df = generate_features(df)

        # -----------------------------
        # Pattern Detection
        # -----------------------------
        patterns = run_pattern_engine(df)

        if patterns is None:
            patterns = []

        patterns = rank_patterns(patterns)
        top_patterns = get_top_patterns(patterns)

        # ------------------------------------------------
        # Glucose Overview Metrics
        # ------------------------------------------------
        st.subheader("📊 Glucose Overview")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Average Glucose", f"{round(df.attrs['daily_mean'],1)} mg/dL")
        c2.metric("Variability (STD)", f"{round(df.attrs['std_glucose'],1)}")
        c3.metric("Maximum", f"{round(df.attrs['daily_max'],1)}")
        c4.metric("Minimum", f"{round(df.attrs['daily_min'],1)}")

        # ------------------------------------------------
        # Dashboard Layout
        # ------------------------------------------------
        col1, col2, col3 = st.columns([1.3,2,1.3])

        # -----------------------------
        # Top Clinical Patterns
        # -----------------------------
        with col1:

            st.subheader("🏥 Top Clinical Patterns")

            if not top_patterns:
                st.info("No significant patterns detected")

            else:
                for i, p in enumerate(top_patterns, start=1):
                    pattern_card(i, p)

        # -----------------------------
        # Glucose Trend
        # -----------------------------
        with col2:

            st.subheader("📈 Glucose Trend")

            fig = plot_glucose(df)

            st.plotly_chart(fig, use_container_width=True)

        # -----------------------------
        # Clinical Summary
        # -----------------------------
        with col3:

            st.subheader("🧑‍⚕️ Clinical Summary")

            summary_points = []
            recommendations = []

            for p in top_patterns:

                name = p.get("name","")

                if "Hyperglycemia" in name:
                    summary_points.append(
                        "Persistent high glucose levels detected."
                    )
                    recommendations.append(
                        "Review carbohydrate intake and insulin dosing."
                    )

                elif "Hypoglycemia" in name:
                    summary_points.append(
                        "Low glucose episodes detected."
                    )
                    recommendations.append(
                        "Assess medication timing and meal spacing."
                    )

                elif "Variability" in name:
                    summary_points.append(
                        "Glucose variability appears high."
                    )
                    recommendations.append(
                        "Consider stabilizing meal composition and insulin schedule."
                    )

                elif "Spike" in name:
                    summary_points.append(
                        "Significant post-meal glucose spikes observed."
                    )
                    recommendations.append(
                        "Meal carbohydrate load may be excessive."
                    )

            summary_points = list(set(summary_points))
            recommendations = list(set(recommendations))

            if summary_points:

                st.markdown("**Clinical Interpretation**")

                for s in summary_points:
                    st.write(f"• {s}")

                st.markdown("**Areas for Physician Review**")

                for r in recommendations:
                    st.write(f"• {r}")

            else:
                st.info("No major clinical risks detected.")

        # ------------------------------------------------
        # Glycemic Heatmap
        # ------------------------------------------------
        st.subheader("🔥 Glycemic Heatmap")

        fig2 = glucose_heatmap(df)

        st.plotly_chart(fig2, use_container_width=True)

        st.caption(
        "Blue: Hypoglycemia (<70) | Green: Normal (70–140) | Yellow: Borderline (140–180) | Red: Hyperglycemia (>180)"
        )

        # ------------------------------------------------
        # Meal Response Chart
        # ------------------------------------------------
        st.subheader("🍽 Meal Response Pattern")

        fig3 = meal_response_chart(df)

        st.plotly_chart(fig3, use_container_width=True)

        # ------------------------------------------------
        # All Detected Patterns Table
        # ------------------------------------------------
        st.subheader("📊 All Detected Patterns")

        if patterns:

            pattern_df = pd.DataFrame(patterns)

            if "score" in pattern_df.columns:
                pattern_df = pattern_df.sort_values("score", ascending=False)

            st.dataframe(
                make_streamlit_safe(pattern_df),
                height=300,
                use_container_width=True
            )

        else:
            st.info("No patterns detected")

        # ------------------------------------------------
        # Dataset Viewer
        # ------------------------------------------------
        with st.expander("View Processed Dataset"):

            st.dataframe(
                make_streamlit_safe(df),
                use_container_width=True
            )

    except Exception as e:

        st.error("Error processing file")
        st.exception(e)