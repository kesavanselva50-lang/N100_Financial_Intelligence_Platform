import pandas as pd


def normalize(series):
    """
    Normalize a pandas Series to 0-100.
    """

    s = series.fillna(0)

    minimum = s.min()
    maximum = s.max()

    if maximum == minimum:
        return pd.Series(50, index=s.index)

    return ((s - minimum) / (maximum - minimum)) * 100


def inverse_normalize(series):
    """
    Lower value = better.
    Used for Debt/Equity.
    """

    return 100 - normalize(series)


def composite_score(df):

    roe = normalize(df["return_on_equity_pct"])

    npm = normalize(df["net_profit_margin_pct"])

    fcf = normalize(df["free_cash_flow_cr"])

    asset = normalize(df["asset_turnover"])

    icr = normalize(df["interest_coverage"].fillna(999))

    debt = inverse_normalize(df["debt_to_equity"])

    score = (
        roe * 0.30 +
        npm * 0.20 +
        fcf * 0.20 +
        asset * 0.10 +
        icr * 0.10 +
        debt * 0.10
    )

    return score.round(2)