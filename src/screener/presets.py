from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()


def quality_compounder():

    df = engine.apply_filters()

    return df[
        (df["return_on_equity_pct"] > 20) &
        (df["debt_to_equity"] < 0.5) &
        (df["free_cash_flow_cr"] > 100) &
        (df["asset_turnover"] > 1.5)
    ]


def value_pick():

    df = engine.apply_filters()

    return df[
        (df["pe_ratio"] < 20) &
        (df["pb_ratio"] < 3)
    ]


def growth_accelerator():

    df = engine.apply_filters()

    return df[
        (df["return_on_equity_pct"] > 20) &
        (df["asset_turnover"] > 1.5)
    ]


def dividend_champion():

    df = engine.apply_filters()

    return df[
        (df["dividend_payout_ratio_pct"] > 40) &
        (df["dividend_payout_ratio_pct"] < 80) &
        (df["free_cash_flow_cr"] > 100)
    ]


def debt_free_bluechip():

    df = engine.apply_filters()

    return df[
        (df["debt_to_equity"] == 0) &
        (df["return_on_equity_pct"] > 25)
    ]


def turnaround_watch():

    df = engine.apply_filters()

    return df[
        (df["free_cash_flow_cr"] > 200) &
        (df["return_on_equity_pct"] > 15)
    ]