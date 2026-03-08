import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import os
import sys

# -------------------------------------------------------
# PROJECT PATH
# -------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db_connection import engine


# -------------------------------------------------------
# NORMALIZE STATE FUNCTION
# -------------------------------------------------------
def normalize_state(x):
    return (
        x.lower()
        .replace("-", " ")
        .replace("&", "and")
        .replace("  ", " ")
        .strip()
    )


# -------------------------------------------------------
# LOAD GEOJSON
# -------------------------------------------------------
@st.cache_data
def load_geojson():
    geo_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(geo_url)
    return json.loads(response.text)


# -------------------------------------------------------
# LOAD FILTER DATA
# -------------------------------------------------------
@st.cache_data
def load_filters():
    years = pd.read_sql(
        "SELECT DISTINCT year FROM fact_aggregated_transaction ORDER BY year",
        engine,
    )

    quarters = pd.read_sql(
        "SELECT DISTINCT quarter FROM fact_aggregated_transaction ORDER BY quarter",
        engine,
    )

    return years, quarters


# -------------------------------------------------------
# LOAD MAP DATA
# -------------------------------------------------------
@st.cache_data
def load_map_data(year, quarter, column):
    query = f"""
        SELECT state,
               SUM({column}) AS total_metric
        FROM fact_aggregated_transaction
        WHERE year=%s AND quarter=%s
        GROUP BY state
    """

    df = pd.read_sql(query, engine, params=(year, quarter))
    return df


# -------------------------------------------------------
# MAIN DASHBOARD FUNCTION
# -------------------------------------------------------
def show():

    st.title("🇮🇳 India Transaction Intelligence Map")
    st.markdown("---")

    # Load GeoJSON
    india_geojson = load_geojson()

    # Load filters
    years, quarters = load_filters()

    # -------------------------------------------------------
    # FILTER UI
    # -------------------------------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_year = st.selectbox(
            "Select Year",
            years["year"],
            key="map_year"
        )

    with col2:
        selected_quarter = st.selectbox(
            "Select Quarter",
            quarters["quarter"],
            key="map_quarter"
        )

    with col3:
        metric_option = st.radio(
            "Select Metric",
            ("Transaction Value", "Transaction Count"),
            horizontal=True,
            key="map_metric"
        )

    st.markdown("---")

    # -------------------------------------------------------
    # COLUMN MAP
    # -------------------------------------------------------
    column_map = {
        "Transaction Value": "transaction_amount",
        "Transaction Count": "transaction_count",
    }

    column = column_map[metric_option]

    # -------------------------------------------------------
    # LOAD DATA
    # -------------------------------------------------------
    map_df = load_map_data(selected_year, selected_quarter, column)

    if map_df.empty:
        st.warning("No data available for selected filters.")
        return

    # -------------------------------------------------------
    # SPECIAL STATE FIX
    # -------------------------------------------------------
    special_cases = {
        "andaman-&-nicobar-islands": "Andaman & Nicobar"
    }

    map_df["state_override"] = map_df["state"].map(special_cases)
    map_df["state_final"] = map_df["state_override"].fillna(map_df["state"])

    # -------------------------------------------------------
    # CLEAN STATE NAMES
    # -------------------------------------------------------
    map_df["state_clean"] = map_df["state_final"].apply(normalize_state)

    # -------------------------------------------------------
    # GEOJSON LOOKUP
    # -------------------------------------------------------
    geo_lookup = {}

    for feature in india_geojson["features"]:
        geo_name = feature["properties"]["ST_NM"]
        geo_lookup[normalize_state(geo_name)] = geo_name

    map_df["state_geo"] = map_df["state_clean"].map(geo_lookup)

    # Warn for missing states
    missing = map_df[map_df["state_geo"].isna()]
    if not missing.empty:
        st.warning(f"Unmatched states: {missing['state'].unique()}")

    # -------------------------------------------------------
    # CHOROPLETH MAP
    # -------------------------------------------------------
    fig = px.choropleth(
        map_df,
        geojson=india_geojson,
        locations="state_geo",
        featureidkey="properties.ST_NM",
        color="total_metric",
        hover_name="state_geo",
        hover_data={"total_metric": ":,"},
        color_continuous_scale="Viridis",
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig.update_layout(
        template="plotly_dark",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar=dict(title=metric_option)
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------
    # INSIGHTS
    # -------------------------------------------------------
    st.markdown("---")
    st.subheader("📊 Key Insights")

    top_state = map_df.sort_values("total_metric", ascending=False).iloc[0]
    bottom_state = map_df.sort_values("total_metric").iloc[0]

    st.markdown(f"""
    **Top Performing State:** {top_state['state_geo']}  
    **Highest {metric_option}:** {top_state['total_metric']:,.0f}

    **Lowest Performing State:** {bottom_state['state_geo']}  
    **Lowest {metric_option}:** {bottom_state['total_metric']:,.0f}
    """)