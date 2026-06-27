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