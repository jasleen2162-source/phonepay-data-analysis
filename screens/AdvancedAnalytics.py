import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# -------------------------------------------------------
# PROJECT PATH
# -------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db_connection import engine
from KPIStyles import apply_custom_styles


# -------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------
def normalize_state_name(name):
    return name.replace("-", " ").title()


# -------------------------------------------------------
# CACHE DATA LOADERS
# -------------------------------------------------------
@st.cache_data
def load_states():
    path = "./pulse/data/map/transaction/hover/country/india/state/"
    return sorted(os.listdir(path))


@st.cache_data
def load_district_distribution(state, table, column):
    query = f"""
        SELECT district, SUM({column}) AS total_value
        FROM {table}
        WHERE state=%s
        GROUP BY district
    """
    return pd.read_sql(query, engine, params=(state,))


@st.cache_data
def load_correlation_data(state):
    query = """
        SELECT t.district,
               SUM(t.transaction_amount) AS transactions,
               SUM(u.registered_users) AS users,
               SUM(i.insurance_count) AS insurance
        FROM fact_map_transaction t
        LEFT JOIN fact_map_user u
            ON t.state=u.state AND t.district=u.district
        LEFT JOIN fact_map_insurance i
            ON t.state=i.state AND t.district=i.district
        WHERE t.state=%s
        GROUP BY t.district
    """
    return pd.read_sql(query, engine, params=(state,))


# -------------------------------------------------------
# MAIN DASHBOARD
# -------------------------------------------------------
def show():

    apply_custom_styles()

    st.title("📊 Advanced Analytics Dashboard")

    # -------------------------------------------------------
    # STATE SELECTION
    # -------------------------------------------------------
    states = load_states()

    selected_state = st.selectbox(
        "Select State for Detailed Analysis",
        states,
        key="analytics_state"
    )

    state_clean = normalize_state_name(selected_state)

    # -------------------------------------------------------
    # DISTRIBUTION & OUTLIERS
    # -------------------------------------------------------
    st.markdown("---")
    st.subheader(f"📊 Distribution & Outliers - {state_clean}")

    district_metric_map = {
        "Transaction Value": ("fact_map_transaction", "transaction_amount"),
        "Transaction Count": ("fact_map_transaction", "transaction_count"),
        "Registered Users": ("fact_map_user", "registered_users"),
        "Insurance Count": ("fact_map_insurance", "insurance_count")
    }

    dist_metric_option = st.radio(
        "Select Metric for Distribution",
        list(district_metric_map.keys()),
        horizontal=True,
        key="analytics_dist_metric"
    )

    table_dist, column_dist = district_metric_map[dist_metric_option]

    district_df = load_district_distribution(
        state_clean,
        table_dist,
        column_dist
    )

    if district_df.empty:
        st.warning("No district data available.")
        return

    # -------------------------------------------------------
    # BOX PLOT
    # -------------------------------------------------------
    fig_box = px.box(
        district_df,
        y="total_value",
        points="all",
        title=f"{dist_metric_option} Distribution Across Districts in {state_clean}",
    )

    st.plotly_chart(fig_box, use_container_width=True)

    # -------------------------------------------------------
    # HISTOGRAM
    # -------------------------------------------------------
    fig_hist = px.histogram(
        district_df,
        x="total_value",
        nbins=15,
        title=f"{dist_metric_option} Histogram Across Districts"
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    # -------------------------------------------------------
    # TOP N DISTRICTS
    # -------------------------------------------------------
    st.markdown("---")
    st.subheader(f"🏆 Top Districts - {state_clean}")

    top_n = st.slider(
        "Select Top N Districts",
        min_value=3,
        max_value=10,
        value=5,
        key="analytics_top_n"
    )

    top_districts_df = (
        district_df
        .sort_values("total_value", ascending=False)
        .head(top_n)
    )

    # -------------------------------------------------------
    # TREEMAP
    # -------------------------------------------------------
    fig_tree = px.treemap(
        top_districts_df,
        path=["district"],
        values="total_value",
        color="total_value",
        color_continuous_scale="Viridis",
        title=f"Top {top_n} Districts by {dist_metric_option}"
    )

    st.plotly_chart(fig_tree, use_container_width=True)

    # -------------------------------------------------------
    # PIE CHART
    # -------------------------------------------------------
    fig_pie = px.pie(
        top_districts_df,
        names="district",
        values="total_value",
        title=f"{dist_metric_option} Share of Top {top_n} Districts"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # -------------------------------------------------------
    # CORRELATION ANALYSIS
    # -------------------------------------------------------
    st.markdown("---")
    st.subheader(f"🔗 Correlation Analysis - {state_clean}")

    corr_df = load_correlation_data(state_clean)

    if corr_df.empty:
        st.warning("No correlation data available.")
        return

    fig_scatter = px.scatter(
        corr_df,
        x="users",
        y="transactions",
        size="insurance",
        color="district",
        hover_name="district",
        title="Transactions vs Users vs Insurance per District",
        size_max=40
    )

    st.plotly_chart(fig_scatter, use_container_width=True)