from src.analytics.ratios import asset_turnover, debt_to_equity, icr_label, icr_warning_flag, interest_coverage_ratio, net_debt, net_profit_margin


def test_net_profit_margin():

    assert round(
        net_profit_margin(100, 500),
        2
    ) == 20.00


def test_net_profit_margin_zero_sales():

    assert net_profit_margin(
        100,
        0
    ) is None
from src.analytics.ratios import operating_profit_margin


def test_operating_profit_margin():

    assert round(
        operating_profit_margin(200, 1000),
        2
    ) == 20.00


def test_operating_profit_margin_zero_sales():

    assert operating_profit_margin(
        200,
        0
    ) is None    
from src.analytics.ratios import return_on_equity


def test_roe():

    assert round(
        return_on_equity(
            100,
            300,
            200
        ),
        2
    ) == 20.00


def test_roe_negative_equity():

    assert return_on_equity(
        100,
        -300,
        100
    ) is None    

def test_debt_to_equity():

    assert (
        debt_to_equity(
            100,
            50,
            50
        )
        == 1
    )

def test_debt_to_equity_debt_free():

    assert (
        debt_to_equity(
            0,
            100,
            100
        )
        == 0
    )

def test_debt_to_equity_negative_equity():

    assert (
        debt_to_equity(
            100,
            -50,
            20
        )
        is None
    )

def test_interest_coverage():

    assert (
        interest_coverage_ratio(
            100,
            20,
            10
        )
        == 12
    )

def test_interest_zero():

    assert (
        interest_coverage_ratio(
            100,
            20,
            0
        )
        is None
    )

def test_debt_free_label():

    assert icr_label(0) == "Debt Free"
    
def test_net_debt():

    assert (
        net_debt(
            500,
            150
        )
        == 350
    )

def test_asset_turnover():

    assert (
        asset_turnover(
            1000,
            500
        )
        == 2
    )

def test_icr_warning_true():

    assert icr_warning_flag(1.2) is True


def test_icr_warning_false():

    assert icr_warning_flag(2.5) is False