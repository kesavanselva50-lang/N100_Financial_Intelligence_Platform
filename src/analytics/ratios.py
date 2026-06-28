"""
Financial Ratio Engine
Sprint 2 - Day 08
"""

def net_profit_margin(
    net_profit,
    sales
):
    """
    Net Profit Margin (%)
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100

def operating_profit_margin(
    operating_profit,
    sales
):

    if sales == 0:
        return None

    return (
        operating_profit
        / sales
    ) * 100
def return_on_equity(
    net_profit,
    equity,
    reserves
):

    capital = equity + reserves

    if capital <= 0:
        return None

    return (
        net_profit
        / capital
    ) * 100
def debt_to_equity(
    borrowings,
    equity_capital,
    reserves
):
    """
    Debt to Equity Ratio
    """

    equity = equity_capital + reserves

    if borrowings == 0:
        return 0

    if equity <= 0:
        return None

    return borrowings / equity
def high_leverage_flag(
    debt_to_equity,
    broad_sector
):
    """
    High leverage warning
    """

    if broad_sector == "Financials":
        return False

    return debt_to_equity > 5
def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio
    """

    if interest == 0:
        return None

    return (
        operating_profit
        + other_income
    ) / interest
def icr_label(
    interest
):
    """
    Debt Free label
    """

    if interest == 0:
        return "Debt Free"

    return ""
def net_debt(
    borrowings,
    investments
):
    """
    Net Debt
    """

    return borrowings - investments
def asset_turnover(
    sales,
    total_assets
):
    """
    Asset Turnover Ratio
    """

    if total_assets == 0:
        return None

    return sales / total_assets
def icr_warning_flag(icr):
    """
    Returns True if the Interest Coverage Ratio is below 1.5.
    """

    if icr is None:
        return False

    return icr < 1.5