import streamlit as st

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="PhonePe Intelligence Platform",
    layout="wide"
)

# -------------------------------------------------------
# REMOVE SIDEBAR
# -------------------------------------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# CUSTOM NAVBAR STYLE
# -------------------------------------------------------
st.markdown("""
<style>

.navbar {
    display: flex;
    justify-content: center;
    background: linear-gradient(90deg, #5f2c82, #49a09d);
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.nav-item {
    color: white;
    font-size: 18px;
    font-weight: 500;
    margin: 0 25px;
    cursor: pointer;
    transition: 0.3s;
}

.nav-item:hover {
    color: #ffd700;
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# SESSION STATE DEFAULT PAGE
# -------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "India Map"

# -------------------------------------------------------
# NAVIGATION BAR
# -------------------------------------------------------
col1, col2, col3 , col4= st.columns(4)

with col1:
    if st.button("🇮🇳 India Map"):
        st.session_state.page = "India Map"

with col2:
    if st.button("📊 Executive Overview"):
        st.session_state.page = "Executive Overview"

with col3:
    if st.button("📈 Advanced Analytics"):
        st.session_state.page = "Advanced Analytics"

with col4:
    if st.button("📋 Details"):
        st.session_state.page = "Details"


st.markdown("---")

# -------------------------------------------------------
# LOAD SELECTED SCREEN
# -------------------------------------------------------

if st.session_state.page == "India Map":
    from screens import MapDashboard
    MapDashboard.show()

elif st.session_state.page == "Details":
    from screens import Details
    Details.show()

elif st.session_state.page == "Executive Overview":
    from screens import KPIDashboard
    KPIDashboard.show()

elif st.session_state.page == "Advanced Analytics":
    from screens import AdvancedAnalytics
    AdvancedAnalytics.show()
    


