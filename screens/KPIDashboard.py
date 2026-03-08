import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db_connection import engine
from KPIStyles import apply_custom_styles, kpi_card_html


def normalize_state_name(name):
    return name.replace("-", " ").title()


@st.cache_data
def run_query(query, params=None):
    return pd.read_sql(query, engine, params=params)


def show():

    apply_custom_styles()

    st.title("📊 Executive Overview Dashboard")

    # -----------------------------
    # KPI QUERIES
    # -----------------------------

    total_txn_value = run_query(
        "SELECT SUM(transaction_amount) FROM fact_aggregated_transaction"
    ).iloc[0, 0]

    total_txn_count = run_query(
        "SELECT SUM(transaction_count) FROM fact_aggregated_transaction"
    ).iloc[0, 0]

    total_users = run_query(
        "SELECT SUM(registered_users) FROM fact_aggregated_user"
    ).iloc[0, 0]

    total_insurance = run_query(
        "SELECT SUM(insurance_amount) FROM fact_aggregated_insurance"
    ).iloc[0, 0]

    # -----------------------------
    # KPI DISPLAY
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            kpi_card_html("💰 Total Transaction Value", f"₹ {total_txn_value:,.0f}"),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            kpi_card_html(
                "🔄 Total Transactions",
                f"{total_txn_count:,.0f}",
                gradient="linear-gradient(90deg, #ff758c, #ff7eb3)",
            ),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            kpi_card_html(
                "👥 Total Registered Users",
                f"{total_users:,.0f}",
                gradient="linear-gradient(90deg, #43e97b, #38f9d7)",
            ),
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            kpi_card_html(
                "🛡 Total Insurance Value",
                f"₹ {total_insurance:,.0f}",
                gradient="linear-gradient(90deg, #fa709a, #fee140)",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # -----------------------------
    # YEAR-WISE GROWTH
    # -----------------------------

    st.subheader("📈 Year-wise Growth Comparison")

    growth_query = """
    SELECT 
        t.year,
        t.total_value,
        t.total_count,
        u.total_users,
        i.total_insurance
    FROM
    (
        SELECT year,
            SUM(transaction_amount) AS total_value,
            SUM(transaction_count) AS total_count
        FROM fact_aggregated_transaction
        GROUP BY year
    ) t
    LEFT JOIN
    (
        SELECT year,
            SUM(registered_users) AS total_users
        FROM fact_aggregated_user
        GROUP BY year
    ) u ON t.year = u.year
    LEFT JOIN
    (
        SELECT year,
            SUM(insurance_amount) AS total_insurance
        FROM fact_aggregated_insurance
        GROUP BY year
    ) i ON t.year = i.year
    ORDER BY t.year
    """

    growth_df = run_query(growth_query)

    metric_option = st.radio(
        "Select Growth Metric",
        (
            "Transaction Value",
            "Transaction Count",
            "Registered Users",
            "Insurance Value",
        ),
        horizontal=True,
        key="yearwise_metric",
    )

    metric_map = {
        "Transaction Value": "total_value",
        "Transaction Count": "total_count",
        "Registered Users": "total_users",
        "Insurance Value": "total_insurance",
    }

    selected_column = metric_map[metric_option]

    fig = px.line(
        growth_df,
        x="year",
        y=selected_column,
        markers=True,
        title=f"Year-wise Growth - {metric_option}",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # TOP STATES
    # -----------------------------

    st.subheader("🏆 Top 5 States Analysis")

    metric_choice = st.radio(
        "Select Metric",
        (
            "Transaction Value",
            "Transaction Count",
            "Registered Users",
            "Insurance Value",
        ),
        horizontal=True,
        key="top_states_metric",
    )

    metric_table_map = {
        "Transaction Value": ("fact_aggregated_transaction", "transaction_amount"),
        "Transaction Count": ("fact_aggregated_transaction", "transaction_count"),
        "Registered Users": ("fact_aggregated_user", "registered_users"),
        "Insurance Value": ("fact_aggregated_insurance", "insurance_amount"),
    }

    table, column = metric_table_map[metric_choice]

    top_states_query = f"""
    SELECT state, SUM({column}) AS total_metric
    FROM {table}
    GROUP BY state
    ORDER BY total_metric DESC
    LIMIT 5
    """

    top_states_df = run_query(top_states_query)

    fig_states = px.bar(
        top_states_df,
        x="state",
        y="total_metric",
        color="state",
        text_auto=True,
        title=f"Top 5 States - {metric_choice}",
    )

    st.plotly_chart(fig_states, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # STATE & DISTRICT ANALYSIS
    # -----------------------------

    path = "./pulse/data/map/transaction/hover/country/india/state/"
    state_list = sorted(os.listdir(path))

    col_state, col_district = st.columns(2)

    with col_state:

        st.subheader("State Analysis")

        selected_state = st.selectbox("Select State", state_list)

        table, column = metric_table_map[metric_choice]

        state_query = f"""
        SELECT year, SUM({column}) AS total_value
        FROM {table}
        WHERE state = %s
        GROUP BY year
        ORDER BY year
        """

        state_df = run_query(
            state_query, params=(normalize_state_name(selected_state),)
        )

        state_df["YoY Growth %"] = state_df["total_value"].pct_change() * 100

        fig_state = px.line(
            state_df,
            x="year",
            y="total_value",
            markers=True,
            title=f"{metric_choice} Trend - {selected_state}",
        )

        st.plotly_chart(fig_state, use_container_width=True)

        st.dataframe(state_df, use_container_width=True)

    # -----------------------------
    # DISTRICT ANALYSIS
    # -----------------------------

    with col_district:

        st.subheader("District Analysis")

        district_metric_map = {
            "Transaction Value": ("fact_map_transaction", "transaction_amount"),
            "Transaction Count": ("fact_map_transaction", "transaction_count"),
            "Registered Users": ("fact_map_user", "registered_users"),
            "Insurance Count": ("fact_map_insurance", "insurance_count"),
        }

        district_metric_option = st.radio(
            "Select District Metric",
            (
                "Transaction Value",
                "Transaction Count",
                "Registered Users",
                "Insurance Count",
            ),
            horizontal=True,
            key="district_metric",
        )

        table_district, column_district = district_metric_map[district_metric_option]

        district_query = """
        SELECT DISTINCT district
        FROM fact_map_transaction
        WHERE state = %s
        ORDER BY district
        """

        districts = run_query(
            district_query, params=(normalize_state_name(selected_state),)
        )

        selected_district = st.selectbox("Select District", districts["district"])

        growth_query = f"""
        SELECT year, SUM({column_district}) AS total_value
        FROM {table_district}
        WHERE state = %s AND district = %s
        GROUP BY year
        ORDER BY year
        """

        district_df = run_query(
            growth_query,
            params=(normalize_state_name(selected_state), selected_district),
        )

        district_df["YoY Growth %"] = district_df["total_value"].pct_change() * 100

        fig_district = px.line(
            district_df,
            x="year",
            y="total_value",
            markers=True,
            title=f"{district_metric_option} Trend - {selected_district}",
        )

        st.plotly_chart(fig_district, use_container_width=True)

        st.dataframe(district_df, use_container_width=True)