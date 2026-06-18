"""
Data Normalisation Functions
"""

def normalize_year(value):
    if value is None:
        return None

    value = str(value).strip()

    if "-" in value:
        return value.split("-")[0]

    return value


def normalize_ticker(value):
    if value is None:
        return None

    return str(value).strip().upper()