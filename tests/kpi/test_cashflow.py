from src.analytics.cashflow_kpis import *


def test_free_cash_flow():

    assert free_cash_flow(
        500,
        -200
    ) == 300


def test_cfo_quality_high():

    assert (
        cfo_quality_score(
            120,
            100
        )
        == "High Quality"
    )


def test_cfo_quality_moderate():

    assert (
        cfo_quality_score(
            70,
            100
        )
        == "Moderate"
    )


def test_cfo_quality_risk():

    assert (
        cfo_quality_score(
            20,
            100
        )
        == "Accrual Risk"
    )


def test_capex_asset_light():

    assert (
        capex_intensity(
            -20,
            1000
        )
        == "Asset Light"
    )


def test_capex_capital_intensive():

    assert (
        capex_intensity(
            -200,
            1000
        )
        == "Capital Intensive"
    )


def test_fcf_conversion():

    assert (
        fcf_conversion(
            300,
            600
        )
        == 50
    )


def test_fcf_conversion_none():

    assert (
        fcf_conversion(
            300,
            0
        )
        is None
    )

def test_reinvestor():

    assert (
        capital_allocation_pattern(
            100,
            -50,
            -20
        )
        == "Reinvestor"
    )


def test_shareholder_returns():

    assert (
        capital_allocation_pattern(
            100,
            -50,
            -20,
            True
        )
        == "Shareholder Returns"
    )


def test_distress():

    assert (
        capital_allocation_pattern(
            -100,
            50,
            20
        )
        == "Distress Signal"
    )


def test_growth_debt():

    assert (
        capital_allocation_pattern(
            -50,
            -20,
            80
        )
        == "Growth Funded by Debt"
    )


def test_cash_accumulator():

    assert (
        capital_allocation_pattern(
            100,
            20,
            10
        )
        == "Cash Accumulator"
    )


def test_pre_revenue():

    assert (
        capital_allocation_pattern(
            -100,
            -50,
            -20
        )
        == "Pre-Revenue"
    )


def test_mixed():

    assert (
        capital_allocation_pattern(
            100,
            -20,
            50
        )
        == "Mixed"
    )