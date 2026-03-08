import streamlit as st
import pandas as pd
from database.db_connection import engine


# -------------------------------------------------------
# LOAD YEARS (Aggregated Data)
# -------------------------------------------------------
@st.cache_data
def load_years_agg():
    df = pd.read_sql(
        "SELECT DISTINCT year FROM fact_aggregated_transaction ORDER BY year",
        engine
    )
    return df["year"].tolist()


# -------------------------------------------------------
# LOAD YEARS (District Data)
# -------------------------------------------------------
@st.cache_data
def load_years_map():
    df = pd.read_sql(
        "SELECT DISTINCT year FROM fact_map_transaction ORDER BY year",
        engine
    )
    return df["year"].tolist()


# -------------------------------------------------------
# LOAD STATES (Aggregated)
# -------------------------------------------------------
@st.cache_data
def load_states_agg():
    df = pd.read_sql(
        "SELECT DISTINCT state FROM fact_aggregated_transaction ORDER BY state",
        engine
    )
    return df["state"].tolist()


# -------------------------------------------------------
# LOAD STATES (District Level)
# -------------------------------------------------------
@st.cache_data
def load_states_map():
    df = pd.read_sql(
        "SELECT DISTINCT state FROM fact_map_transaction ORDER BY state",
        engine
    )
    return df["state"].tolist()


# -------------------------------------------------------
# LOAD DISTRICTS
# -------------------------------------------------------
@st.cache_data
def load_districts(state):
    query = """
    SELECT DISTINCT district
    FROM fact_map_transaction
    WHERE state=%s
    ORDER BY district
    """
    df = pd.read_sql(query, engine, params=(state,))
    return df["district"].tolist()


# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
@st.cache_data
def load_data(query, params):
    return pd.read_sql(query, engine, params=params)


# -------------------------------------------------------
# MAIN PAGE
# -------------------------------------------------------
def show():

    st.title("📊 India Digital Payments Data Explorer")

    tab1, tab2 = st.tabs([
        "State Level Analysis",
        "District Drilldown"
    ])

# =====================================================
# TAB 1 — STATE LEVEL
# =====================================================

    with tab1:

        st.subheader("State Level Data")

        years = load_years_agg()
        states = load_states_agg()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            mode = st.selectbox(
                "Mode",
                ["Yearly", "Quarterly"],
                key="state_mode"
            )

        with col2:
            start_year, end_year = st.select_slider(
                "Year Range",
                options=years,
                value=(min(years), max(years)),
                key="state_year_range"
            )

        with col3:
            selected_state = st.selectbox(
                "State",
                ["All States"] + states,
                key="state_select"
            )

        with col4:
            metric = st.selectbox(
                "Metric",
                [
                    "Transaction Value",
                    "Transaction Count",
                    "Registered Users",
                    "Insurance Amount"
                ],
                key="metric_select"
            )

        metric_config = {
            "Transaction Value": ("fact_aggregated_transaction", "transaction_amount"),
            "Transaction Count": ("fact_aggregated_transaction", "transaction_count"),
            "Registered Users": ("fact_aggregated_user", "registered_users"),
            "Insurance Amount": ("fact_aggregated_insurance", "insurance_amount")
        }

        table, column = metric_config[metric]

        if mode == "Yearly":

            if selected_state == "All States":

                query = f"""
                SELECT year, state, SUM({column}) AS value
                FROM {table}
                WHERE year BETWEEN %s AND %s
                GROUP BY year, state
                ORDER BY year
                """

                params = (start_year, end_year)

            else:

                query = f"""
                SELECT year, state, SUM({column}) AS value
                FROM {table}
                WHERE year BETWEEN %s AND %s
                AND state=%s
                GROUP BY year, state
                ORDER BY year
                """

                params = (start_year, end_year, selected_state)

        else:

            if selected_state == "All States":

                query = f"""
                SELECT year, quarter, state, SUM({column}) AS value
                FROM {table}
                WHERE year BETWEEN %s AND %s
                GROUP BY year, quarter, state
                ORDER BY year, quarter
                """

                params = (start_year, end_year)

            else:

                query = f"""
                SELECT year, quarter, state, SUM({column}) AS value
                FROM {table}
                WHERE year BETWEEN %s AND %s
                AND state=%s
                GROUP BY year, quarter, state
                ORDER BY year, quarter
                """

                params = (start_year, end_year, selected_state)

        df = load_data(query, params)

        if not df.empty:

            if mode == "Yearly":

                pivot_df = df.pivot_table(
                    index="state",
                    columns="year",
                    values="value",
                    aggfunc="sum"
                )

            else:

                df["period"] = df["year"].astype(str) + " Q" + df["quarter"].astype(str)

                pivot_df = df.pivot_table(
                    index="state",
                    columns="period",
                    values="value",
                    aggfunc="sum"
                )

            st.dataframe(
                pivot_df.style.background_gradient(cmap="viridis"),
                use_container_width=True
            )

        else:
            st.warning("No data available.")

# =====================================================
# TAB 2 — DISTRICT LEVEL
# =====================================================

    with tab2:

        st.subheader("District Level Data")

        states = load_states_map()
        years = load_years_map()

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            selected_state = st.selectbox(
                "State",
                states,
                key="district_state"
            )

        districts = load_districts(selected_state)

        with col2:
            selected_district = st.selectbox(
                "District",
                ["All Districts"] + districts,
                key="district_select"
            )

        with col3:
            mode = st.selectbox(
                "Mode",
                ["Yearly", "Quarterly"],
                key="district_mode"
            )

        with col4:
            start_year, end_year = st.select_slider(
                "Year Range",
                options=years,
                value=(min(years), max(years)),
                key="district_year_range"
            )

        with col5:
            metric = st.selectbox(
                "Metric",
                [
                    "Transaction Value",
                    "Transaction Count"
                ],
                key="district_metric"
            )

        metric_config = {
            "Transaction Value": "transaction_amount",
            "Transaction Count": "transaction_count"
        }

        column = metric_config[metric]

        if mode == "Yearly":

            query = f"""
            SELECT year, district, SUM({column}) AS value
            FROM fact_map_transaction
            WHERE state=%s
            AND year BETWEEN %s AND %s
            GROUP BY year, district
            """

            params = (selected_state, start_year, end_year)

        else:

            query = f"""
            SELECT year, quarter, district, SUM({column}) AS value
            FROM fact_map_transaction
            WHERE state=%s
            AND year BETWEEN %s AND %s
            GROUP BY year, quarter, district
            ORDER BY year, quarter
            """

            params = (selected_state, start_year, end_year)

        df = load_data(query, params)

        if not df.empty:

            if mode == "Yearly":

                pivot_df = df.pivot_table(
                    index="district",
                    columns="year",
                    values="value",
                    aggfunc="sum"
                )

            else:

                df["period"] = df["year"].astype(str) + " Q" + df["quarter"].astype(str)

                pivot_df = df.pivot_table(
                    index="district",
                    columns="period",
                    values="value",
                    aggfunc="sum"
                )

            st.dataframe(
                pivot_df.style.background_gradient(cmap="viridis"),
                use_container_width=True
            )

        else:
            st.warning("No district data available.")