import sys
from pathlib import Path

import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[3]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.utils.db import get_companies

st.set_page_config(
    page_title="Company Profile",
    page_icon="🏢",
    layout="wide",
)

st.title("🏢 Company Profile")

df = get_companies()

company = st.selectbox(
    "Select Company",
    sorted(df["company_id"].unique())
)

info = df[df["company_id"] == company].iloc[0]

st.markdown("## Company Information")

col1, col2, col3 = st.columns(3)

col1.metric("Company", info["company_id"])
col2.metric("Sector", info["broad_sector"])
col3.metric("Rating", info["rating"])

st.divider()

st.markdown("## Financial Metrics")

k1, k2, k3 = st.columns(3)

k1.metric(
    "ROE %",
    round(info["return_on_equity_pct"], 2)
)

k2.metric(
    "Debt / Equity",
    round(info["debt_to_equity"], 2)
)

k3.metric(
    "Quality Score",
    round(info["composite_quality_score"], 2)
)

st.divider()

st.markdown("## Company Snapshot")

fig = px.bar(
    x=[
        "ROE",
        "Debt/Equity",
        "Quality Score"
    ],
    y=[
        info["return_on_equity_pct"],
        info["debt_to_equity"],
        info["composite_quality_score"]
    ],
    title=company
)

st.plotly_chart(fig, use_container_width=True)