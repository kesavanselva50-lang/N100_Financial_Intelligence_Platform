import streamlit as st
from src.utils.db import get_companies

st.title("🏢 Company Profile")

df = get_companies()

company = st.selectbox(
    "Select Company",
    sorted(df["company_id"].unique())
)

info = df[df["company_id"] == company].iloc[0]

st.markdown("## Company Information")

c1, c2 = st.columns(2)

with c1:
    st.metric("Company", info["company_id"])
    st.metric("Sector", info["broad_sector"])
    st.metric("Rating", info["rating"])

with c2:
    st.metric(
        "Quality Score",
        round(info["composite_quality_score"], 2)
    )

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
    "Free Cash Flow",
    round(info["free_cash_flow_cr"], 2)
)
st.markdown("## Financial Health")

score = float(info["composite_quality_score"])

st.progress(min(score / 100, 1.0))

st.write(f"Composite Quality Score: **{score:.2f}/100**")