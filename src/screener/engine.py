import sqlite3
import pandas as pd
import yaml

from src.screener.score import composite_score


class ScreenerEngine:

    def __init__(
        self,
        db_path="nifty100.db",
        config_path="config/screener_config.yaml"
    ):

        self.conn = sqlite3.connect(db_path)

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)["filters"]

    def load_data(self):

        # Financial Ratios
        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        # Sector Table
        sectors = pd.read_sql(
            """
            SELECT
                company_id,
                broad_sector
            FROM sectors
            """,
            self.conn
        )

        # Market Cap Table
        market = pd.read_sql(
            "SELECT * FROM market_cap",
            self.conn
        )

        # -------------------------
        # Normalize Year
        # -------------------------

        ratios["merge_year"] = (
            ratios["year"]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
            .astype(int)
        )

        market["merge_year"] = (
            market["year"]
            .astype(int)
        )

        # -------------------------
        # Merge Sector
        # -------------------------

        df = ratios.merge(
            sectors,
            on="company_id",
            how="left"
        )

        # -------------------------
        # Merge Market Cap
        # -------------------------

        df = df.merge(
            market,
            on=["company_id", "merge_year"],
            how="left",
            suffixes=("", "_market")
        )

        # -------------------------
        # Keep Latest Financial Year
        # -------------------------

        df = (
            df.sort_values("merge_year")
              .groupby("company_id", as_index=False)
              .tail(1)
              .reset_index(drop=True)
        )

        return df

    def apply_filters(self):

        df = self.load_data()

        c = self.config

        # -------------------------
        # ROE Filter
        # -------------------------

        df = df[
            df["return_on_equity_pct"] >=
            c["roe_min"]
        ]

        # -------------------------
        # Debt Filter
        # Ignore Financial Sector
        # -------------------------

        financials = (
            df["broad_sector"] == "Financials"
        )

        df = df[
            financials |
            (
                df["debt_to_equity"] <=
                c["debt_to_equity_max"]
            )
        ]

        # -------------------------
        # Free Cash Flow
        # -------------------------

        df = df[
            df["free_cash_flow_cr"] >=
            c["free_cash_flow_min"]
        ]

        # -------------------------
        # Asset Turnover
        # -------------------------

        df = df[
            df["asset_turnover"] >=
            c["asset_turnover_min"]
        ]

        # -------------------------
        # Interest Coverage
        # -------------------------

        df["interest_coverage"] = (
            df["interest_coverage"]
            .replace("Debt Free", float("inf"))
        )

        df["interest_coverage"] = pd.to_numeric(
            df["interest_coverage"],
            errors="coerce"
        )

        df = df[
            df["interest_coverage"]
            .fillna(float("inf"))
            >= c["interest_coverage_min"]
        ]

        # -------------------------
        # Composite Score
        # -------------------------

        df["composite_quality_score"] = composite_score(df)

        # -------------------------
        # Overall Rank
        # -------------------------

        df["overall_rank"] = (
            df["composite_quality_score"]
            .rank(
                ascending=False,
                method="dense"
            )
            .astype(int)
        )

        # -------------------------
        # Sector Rank
        # -------------------------

        df["sector_rank"] = (
            df.groupby("broad_sector")[
                "composite_quality_score"
            ]
            .rank(
                ascending=False,
                method="dense"
            )
            .astype(int)
        )

        # -------------------------
        # Percentile
        # -------------------------

        df["percentile"] = (
            df["composite_quality_score"]
            .rank(pct=True)
            * 100
        ).round(2)

        # -------------------------
        # Stock Rating
        # -------------------------

        def get_rating(percentile):

            if percentile >= 95:
                return "★★★★★"

            elif percentile >= 80:
                return "★★★★"

            elif percentile >= 60:
                return "★★★"

            elif percentile >= 40:
                return "★★"

            else:
                return "★"

        df["rating"] = df["percentile"].apply(get_rating)

        # -------------------------
        # Final Sort
        # -------------------------

        df = df.sort_values(
            by="overall_rank"
        )

        return df


if __name__ == "__main__":

    engine = ScreenerEngine()

    result = engine.apply_filters()

    print(
        result[
            [
                "overall_rank",
                "sector_rank",
                "company_id",
                "year",
                "composite_quality_score",
                "percentile",
                "rating",
                "return_on_equity_pct",
                "debt_to_equity",
                "broad_sector"
            ]
        ].head(20)
    )

    print("\nCompanies Found:", len(result))