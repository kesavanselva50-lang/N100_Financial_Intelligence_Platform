import streamlit as st
import plotly.express as px

from src.screener.engine import ScreenerEngine
from src.portfolio.recommend import (
    conservative_portfolio,
    growth_portfolio,
    dividend_portfolio,
    value_portfolio,
)

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    page_icon="📈",
    layout="wide"
)

engine = ScreenerEngine()
df = engine.apply_filters()

# -------------------------------
# Sidebar Filters
# -------------------------------

st.sidebar.header("Dashboard Filters")

selected_sector = st.sidebar.selectbox(
    "Select Sector",
    ["All"] + sorted(df["broad_sector"].dropna().unique().tolist())
)

minimum_score = st.sidebar.slider(
    "Minimum Composite Score",
    min_value=0.0,
    max_value=float(df["composite_quality_score"].max()),
    value=0.0
)

if selected_sector != "All":
    df = df[df["broad_sector"] == selected_sector]

df = df[df["composite_quality_score"] >= minimum_score]

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.title("📈 N100 Financial Intelligence Platform")
st.markdown("### Professional Stock Screener & Portfolio Analytics")

st.divider()

# ----------------------------------------------------
# Portfolio Selection
# ----------------------------------------------------

portfolio_type = st.sidebar.selectbox(
    "Select Portfolio",
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

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

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

# ----------------------------------------------------
# Company Table
# ----------------------------------------------------

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

# ----------------------------------------------------
# Top 10 Chart
# ----------------------------------------------------

top10 = df.head(10)

st.subheader("📊 Top 10 Companies")

fig = px.bar(
    top10,
    x="company_id",
    y="composite_quality_score",
    color="broad_sector",
    title="Top 10 Companies by Composite Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Sector Distribution
# ----------------------------------------------------

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
    title="Companies by Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📊 Composite Score Distribution")

fig = px.histogram(
    df,
    x="composite_quality_score",
    nbins=20,
    title="Distribution of Composite Scores"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Portfolio Allocation
# ----------------------------------------------------

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
    title=f"{portfolio_type} Portfolio Allocation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Top Quality Stocks
# ----------------------------------------------------

st.subheader("⭐ Top Quality Stocks")

st.dataframe(
    top10[
        [
            "overall_rank",
            "company_id",
            "broad_sector",
            "rating",
            "composite_quality_score"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------
# Recommended Portfolio
# ----------------------------------------------------

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
st.subheader("📈 ROE vs Debt to Equity")

fig = px.scatter(
    df,
    x="debt_to_equity",
    y="return_on_equity_pct",
    color="broad_sector",
    hover_name="company_id",
    size="composite_quality_score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("⬇ Download Screened Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="screened_companies.csv",
    mime="text/csv"
)