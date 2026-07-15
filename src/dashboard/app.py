import streamlit as st

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

home = st.Page("pages/Home.py", title="Home", icon="🏠")
profile = st.Page("pages/02_Profile.py", title="Profile", icon="🏢")
screener = st.Page("pages/1_Stock_Screener.py", title="Stock Screener", icon="📈")
portfolio = st.Page("pages/2_Portfolio.py", title="Portfolio", icon="💼")
sector = st.Page("pages/3_Sector_Analytics.py", title="Sector Analytics", icon="🏭")
company = st.Page("pages/4_Company_Analytics.py", title="Company Analytics", icon="📊")
about = st.Page("pages/5_About.py", title="About", icon="ℹ️")

pg = st.navigation([
    home,
    profile,
    screener,
    portfolio,
    sector,
    company,
    about,
])

pg.run()