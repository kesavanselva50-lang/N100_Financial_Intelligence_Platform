from src.etl.normaliser import normalize_year

def test_year_range():
    assert normalize_year("2024-25") == "2024"

def test_year_string():
    assert normalize_year("2023") == "2023"

def test_year_spaces():
    assert normalize_year(" 2022 ") == "2022"

def test_year_none():
    assert normalize_year(None) is None

def test_year_integer():
    assert normalize_year(2021) == "2021"