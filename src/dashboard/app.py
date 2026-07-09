# ==========================================================
# Imports
# ==========================================================

import streamlit as st
import plotly.express as px

from src.screener.engine import ScreenerEngine
from src.portfolio.recommend import (
    conservative_portfolio,
    growth_portfolio,
    dividend_portfolio,
    value_portfolio,
)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    page_icon="📈",
    layout="wide"
)

# ==========================================================
# Load Data
# ==========================================================

engine = ScreenerEngine()
df = engine.apply_filters()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("Dashboard Filters")

selected_sector = st.sidebar.selectbox(
    "Select Sector",
    ["All"] + sorted(df["broad_sector"].dropna().unique())
)

minimum_score = st.sidebar.slider(
    "Minimum Composite Score",
    0.0,
    float(df["composite_quality_score"].max()),
    0.0
)

if selected_sector != "All":
    df = df[df["broad_sector"] == selected_sector]

df = df[
    df["composite_quality_score"] >= minimum_score
]

portfolio_type = st.sidebar.selectbox(
    "Portfolio",
    [
        "Conservative",
        "Growth",
        "Dividend",
        "Value"
    ]
)

if portfolio_type == "Conservative":
    portfolio = conservative_portfolio()

elif portfolio_type == "Growth":
    portfolio = growth_portfolio()

elif portfolio_type == "Dividend":
    portfolio = dividend_portfolio()

else:
    portfolio = value_portfolio()

selected_company = st.sidebar.selectbox(
    "Choose Company",
    sorted(df["company_id"].unique())
)

# ==========================================================
# Company Object
# ==========================================================

company = df[
    df["company_id"] == selected_company
].iloc[0]

# ==========================================================
# Header
# ==========================================================

st.title("📈 N100 Financial Intelligence Platform")
st.markdown("### Professional Stock Screener & Portfolio Analytics")

st.divider()

# ==========================================================
# KPI Cards
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Qualified Companies",
    len(df)
)

col2.metric(
    "Highest Score",
    round(df["composite_quality_score"].max(), 2)
)

col3.metric(
    "Average ROE",
    round(df["return_on_equity_pct"].mean(), 2)
)

col4.metric(
    "Sectors",
    df["broad_sector"].nunique()
)

st.divider()

# ==========================================================
# Company Profile
# ==========================================================

st.subheader("🏢 Company Profile")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Company",
    company["company_id"]
)

c2.metric(
    "Sector",
    company["broad_sector"]
)

c3.metric(
    "Rating",
    company["rating"]
)

# ==========================================================
# Financial Health
# ==========================================================

st.subheader("📈 Financial Health")

score = float(company["composite_quality_score"])

st.progress(min(score / 100, 1.0))

st.metric(
    "Composite Quality Score",
    round(score, 2)
)

# ==========================================================
# Key Metrics
# ==========================================================

st.subheader("📊 Key Financial Metrics")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "ROE %",
    round(company["return_on_equity_pct"], 2)
)

m2.metric(
    "Debt/Equity",
    round(company["debt_to_equity"], 2)
)

m3.metric(
    "Asset Turnover",
    round(company["asset_turnover"], 2)
)

m4.metric(
    "Free Cash Flow",
    round(company["free_cash_flow_cr"], 2)
)

# ==========================================================
# Company Table
# ==========================================================

st.subheader("🏆 Top Ranked Companies")

st.dataframe(
    df[
        [
            "overall_rank",
            "company_id",
            "broad_sector",
            "rating",
            "composite_quality_score",
            "return_on_equity_pct",
            "debt_to_equity"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# Charts
# ==========================================================

top10 = df.head(10)

st.subheader("📊 Top 10 Companies")

fig = px.bar(
    top10,
    x="company_id",
    y="composite_quality_score",
    color="broad_sector"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏭 Sector Distribution")

sector = (
    df.groupby("broad_sector")
      .size()
      .reset_index(name="Companies")
)

fig = px.pie(
    sector,
    names="broad_sector",
    values="Companies"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Composite Score Distribution")

fig = px.histogram(
    df,
    x="composite_quality_score",
    nbins=20
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 ROE vs Debt to Equity")

fig = px.scatter(
    df,
    x="debt_to_equity",
    y="return_on_equity_pct",
    color="broad_sector",
    hover_name="company_id",
    size="composite_quality_score"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Sector Leaderboard
# ==========================================================

st.subheader("🏆 Sector Leaderboard")

leaders = (
    df.sort_values(
        "composite_quality_score",
        ascending=False
    )
    .groupby("broad_sector")
    .first()
    .reset_index()
)

st.dataframe(
    leaders[
        [
            "broad_sector",
            "company_id",
            "composite_quality_score"
        ]
    ],
    use_container_width=True
)

# ==========================================================
# Portfolio Allocation
# ==========================================================

st.subheader(f"💼 {portfolio_type} Portfolio Allocation")

allocation = (
    portfolio.groupby("broad_sector")
    .size()
    .reset_index(name="Stocks")
)

fig = px.bar(
    allocation,
    x="broad_sector",
    y="Stocks",
    color="broad_sector"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Portfolio Table
# ==========================================================

st.subheader(f"📦 {portfolio_type} Portfolio")

st.dataframe(
    portfolio[
        [
            "company_id",
            "broad_sector",
            "rating",
            "composite_quality_score"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# Download CSV
# ==========================================================

st.subheader("⬇ Download Screened Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    data=csv,
    file_name="screened_companies.csv",
    mime="text/csv"
)