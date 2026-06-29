"""
CAGR Engine
"""


def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR with edge-case handling.
    """

    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:

        cagr = (
            (
                end_value / start_value
            ) ** (1 / years) - 1
        ) * 100

        return round(cagr, 2), "NORMAL"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "UNKNOWN"

def revenue_cagr(start_sales, end_sales, years):
    return calculate_cagr(start_sales, end_sales, years)


def pat_cagr(start_profit, end_profit, years):
    return calculate_cagr(start_profit, end_profit, years)


def eps_cagr(start_eps, end_eps, years):
    return calculate_cagr(start_eps, end_eps, years)

def insufficient_data(data, required_years):
    """
    Check whether enough yearly records exist.
    """

    if len(data) < required_years:
        return None, "INSUFFICIENT"

    return True, "OK"