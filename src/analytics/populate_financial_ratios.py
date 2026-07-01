import sqlite3
import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capex_intensity,
)

conn = sqlite3.connect("nifty100.db")

pl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)
cf = pd.read_sql("SELECT * FROM cashflow", conn)

df = (
    pl.merge(bs, on=["company_id", "year"])
      .merge(cf, on=["company_id", "year"])
)

records = []

for i, row in enumerate(df.itertuples(index=False), start=1):

    records.append({
        "id": i,
        "company_id": row.company_id,
        "year": row.year,

        "net_profit_margin_pct":
            net_profit_margin(
                row.net_profit,
                row.sales
            ),

        "operating_profit_margin_pct":
            operating_profit_margin(
                row.operating_profit,
                row.sales
            ),

        # FIXED
        "return_on_equity_pct":
            return_on_equity(
                row.net_profit,
                row.equity_capital,
                row.reserves
            ),

        # FIXED (if your function accepts 3 args)
        "debt_to_equity":
            debt_to_equity(
                row.borrowings,
                row.equity_capital,
                row.reserves
            ),

        "interest_coverage":
            interest_coverage_ratio(
                row.operating_profit,
                row.other_income,
                row.interest
            ),

        "asset_turnover":
            asset_turnover(
                row.sales,
                row.total_assets
            ),

        "free_cash_flow_cr":
            free_cash_flow(
                row.operating_activity,
                row.investing_activity
            ),

        "capex_cr":
            capex_intensity(
                row.investing_activity,
                row.sales
            ),

        "earnings_per_share":
            row.eps,

        # Book Value Per Share (temporary)
        "book_value_per_share":
            row.equity_capital + row.reserves,

        "dividend_payout_ratio_pct":
            row.dividend_payout,

        "total_debt_cr":
            row.borrowings,

        "cash_from_operations_cr":
            row.operating_activity,
    })

ratio_df = pd.DataFrame(records)

ratio_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print(f"Inserted {len(ratio_df)} rows into financial_ratios")

conn.close()