# ==========================================================
# Imports
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime

import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.portfolio.recommend import (
    conservative_portfolio,
    growth_portfolio,
    dividend_portfolio,
    value_portfolio,
)
from src.screener.engine import ScreenerEngine


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    page_icon="📈",
    layout="wide",
)

# ==========================================================
# Load Data
# ==========================================================

engine = ScreenerEngine()
df = engine.apply_filters()

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("📊 N100 Analytics")
st.sidebar.success("Version 1.0")

st.sidebar.write(
    "Last Updated:",
    datetime.now().strftime("%d %b %Y")
)

st.sidebar.markdown("---")

# ==========================================================
# Filters
# ==========================================================

st.sidebar.header("Dashboard Filters")

selected_sector = st.sidebar.selectbox(
    "Select Sector",
    ["All"] + sorted(df["broad_sector"].dropna().unique())
)

minimum_score = st.sidebar.slider(
    "Minimum Composite Score",
    min_value=0.0,
    max_value=float(df["composite_quality_score"].max()),
    value=0.0,
)

if selected_sector != "All":
    df = df[df["broad_sector"] == selected_sector]

df = df[
    df["composite_quality_score"] >= minimum_score
]

# ==========================================================
# Portfolio Selection
# ==========================================================

portfolio_type = st.sidebar.selectbox(
    "Portfolio Type",
    [
        "Conservative",
        "Growth",
        "Dividend",
        "Value",
    ],
)

if portfolio_type == "Conservative":
    portfolio = conservative_portfolio()

elif portfolio_type == "Growth":
    portfolio = growth_portfolio()

elif portfolio_type == "Dividend":
    portfolio = dividend_portfolio()

else:
    portfolio = value_portfolio()

# ==========================================================
# Company Selection
# ==========================================================

selected_company = st.sidebar.selectbox(
    "🔍 Search Company",
    sorted(df["company_id"].unique()),
)

company = (
    df[df["company_id"] == selected_company]
    .iloc[0]
)

# ==========================================================
# Dashboard Header
# ==========================================================

st.title("📈 N100 Financial Intelligence Platform")

st.markdown(
    """
### Professional Financial Analytics Dashboard

Analyze Nifty 100 companies using:

- Quality Screening
- Portfolio Recommendation
- Company Analytics
- Sector Analytics
- Financial Health Scores
"""
)

st.divider()

# ==========================================================
# KPI Cards
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Qualified Companies",
    len(df),
)

col2.metric(
    "Highest Score",
    round(df["composite_quality_score"].max(), 2),
)

col3.metric(
    "Average ROE",
    round(df["return_on_equity_pct"].mean(), 2),
)

col4.metric(
    "Sectors",
    df["broad_sector"].nunique(),
)

st.divider()

# ==========================================================
# Company Profile
# ==========================================================

st.subheader("🏢 Company Profile")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Company",
    company["company_id"],
)

c2.metric(
    "Sector",
    company["broad_sector"],
)

c3.metric(
    "Rating",
    company["rating"],
)

# ==========================================================
# Top 5 Quality Companies
# ==========================================================

st.subheader("🏆 Top 5 Quality Companies")

top5 = df.nlargest(
    5,
    "composite_quality_score",
)

st.table(
    top5[
        [
            "company_id",
            "rating",
            "composite_quality_score",
        ]
    ]
)

# ==========================================================
# Financial Health
# ==========================================================

st.subheader("📈 Financial Health")

score = float(
    company["composite_quality_score"]
)

st.progress(
    min(score / 100, 1.0)
)

st.metric(
    "Composite Quality Score",
    round(score, 2),
)

# ==========================================================
# Key Financial Metrics
# ==========================================================

st.subheader("📊 Key Financial Metrics")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "ROE %",
    round(company["return_on_equity_pct"], 2),
)

m2.metric(
    "Debt / Equity",
    round(company["debt_to_equity"], 2),
)

m3.metric(
    "Asset Turnover",
    round(company["asset_turnover"], 2),
)

m4.metric(
    "Free Cash Flow",
    round(company["free_cash_flow_cr"], 2),
)

# ==========================================================
# Company Ranking Table
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
            "debt_to_equity",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

# ==========================================================
# Top 10 ROE
# ==========================================================

st.subheader("📈 Top 10 ROE Companies")

roe = df.nlargest(
    10,
    "return_on_equity_pct",
)

fig = px.bar(
    roe,
    x="company_id",
    y="return_on_equity_pct",
    color="broad_sector",
    title="Top 10 Companies by Return on Equity",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================================
# Top Quality Companies
# ==========================================================

top10 = df.nlargest(
    10,
    "composite_quality_score",
)

st.subheader("🏆 Top 10 Quality Companies")

fig = px.bar(
    top10,
    x="company_id",
    y="composite_quality_score",
    color="broad_sector",
    title="Top 10 Companies by Composite Quality Score",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================================
# Sector Distribution
# ==========================================================

st.subheader("🏭 Sector Distribution")

sector = (
    df.groupby("broad_sector")
      .size()
      .reset_index(name="Companies")
)

fig = px.pie(
    sector,
    names="broad_sector",
    values="Companies",
    title="Distribution of Qualified Companies",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================================
# Composite Score Distribution
# ==========================================================

st.subheader("📊 Composite Score Distribution")

fig = px.histogram(
    df,
    x="composite_quality_score",
    nbins=20,
    title="Composite Quality Score Distribution",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================================
# ROE vs Debt Scatter
# ==========================================================

st.subheader("📈 ROE vs Debt to Equity")

fig = px.scatter(
    df,
    x="debt_to_equity",
    y="return_on_equity_pct",
    color="broad_sector",
    hover_name="company_id",
    size="composite_quality_score",
    title="ROE vs Debt to Equity",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================================
# Sector Leaderboard
# ==========================================================

st.subheader("🏆 Sector Leaderboard")

leaders = (
    df.sort_values(
        "composite_quality_score",
        ascending=False,
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
            "composite_quality_score",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

# ==========================================================
# Sector Statistics
# ==========================================================

st.subheader("📊 Sector Statistics")

sector_stats = (
    df.groupby("broad_sector")
      .agg(
          Companies=("company_id", "count"),
          AvgScore=("composite_quality_score", "mean"),
          AvgROE=("return_on_equity_pct", "mean"),
      )
      .round(2)
)

st.dataframe(
    sector_stats,
    use_container_width=True,
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
    color="broad_sector",
    title=f"{portfolio_type} Portfolio Allocation",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==========================================================
# Recommended Portfolio
# ==========================================================

st.subheader(f"📦 {portfolio_type} Portfolio")

st.dataframe(
    portfolio[
        [
            "company_id",
            "broad_sector",
            "rating",
            "composite_quality_score",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

# ==========================================================
# Portfolio Summary
# ==========================================================

st.subheader("📌 Portfolio Summary")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Stocks",
    len(portfolio),
)

c2.metric(
    "Sectors Covered",
    portfolio["broad_sector"].nunique(),
)

c3.metric(
    "Average Score",
    round(
        portfolio["composite_quality_score"].mean(),
        2,
    ),
)

# ==========================================================
# Download Screened Data
# ==========================================================

st.subheader("⬇ Download Screened Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="screened_companies.csv",
    mime="text/csv",
)

# ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.caption(
    "📈 N100 Financial Intelligence Platform | Built using Python • SQLite • Plotly • Streamlit"
)