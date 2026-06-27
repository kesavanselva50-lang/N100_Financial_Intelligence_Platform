from src.analytics.ratios import net_profit_margin


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