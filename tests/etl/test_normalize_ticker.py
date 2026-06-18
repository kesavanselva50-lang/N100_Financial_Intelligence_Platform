from src.etl.normaliser import normalize_ticker

def test_ticker_upper():
    assert normalize_ticker("tcs") == "TCS"

def test_ticker_spaces():
    assert normalize_ticker(" infy ") == "INFY"

def test_ticker_already_upper():
    assert normalize_ticker("RELIANCE") == "RELIANCE"

def test_ticker_none():
    assert normalize_ticker(None) is None

def test_ticker_mixed():
    assert normalize_ticker("hDfC") == "HDFC"