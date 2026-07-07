from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()


def _latest_data():
    return engine.apply_filters()


def diversify(df, max_per_sector=2):
    """
    Limit each sector to a maximum number of companies
    and return the Top 10 overall.
    """

    return (
        df.groupby("broad_sector", group_keys=False)
          .head(max_per_sector)
          .sort_values("overall_rank")
          .head(10)
    )


def conservative_portfolio():

    df = _latest_data()

    df = df.sort_values(
        "composite_quality_score",
        ascending=False
    )

    return diversify(df)


def growth_portfolio():

    df = _latest_data()

    df = df[
        df["return_on_equity_pct"] > 20
    ]

    df = df.sort_values(
        "return_on_equity_pct",
        ascending=False
    )

    return diversify(df)


def dividend_portfolio():

    df = _latest_data()

    if "dividend_payout_ratio_pct" in df.columns:
        df = df.sort_values(
            "dividend_payout_ratio_pct",
            ascending=False
        )

    return diversify(df)


def value_portfolio():

    df = _latest_data()

    if (
        "pe_ratio" in df.columns and
        "pb_ratio" in df.columns
    ):
        df = df.sort_values(
            ["pe_ratio", "pb_ratio"]
        )

    return diversify(df)