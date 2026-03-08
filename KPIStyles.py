import streamlit as st

def apply_custom_styles():
    st.markdown(
        """
        <style>
        /* Page background & font */
        .stApp {
            background-color: #3b050e;
            font-family: 'Arial', sans-serif;
        }

        /* KPI card style */
        .kpi-card {
            border-radius: 12px;
            padding: 20px;
            color: white;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            font-size: 18px;
            margin-bottom: 15px;
        }

        /* Dropdown & radio button styling */
        .stSelectbox, .stRadio {
            background-color: #3b050e !important;
            border-radius: 8px;
            padding: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        /* Section container */
        .section-container {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.05);
        }

        /* Table container */
        .table-container {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 15px;
            color: #333333;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def kpi_card_html(title, value, gradient="linear-gradient(90deg, #36d1dc, #5b86e5)"):
    return f'<div class="kpi-card" style="background:{gradient}">{title}<br>{value}</div>'