import pandas as pd
from src.etl.validator import Validator


def test_pk_uniqueness():

    df = pd.DataFrame({
        "company_id": [1, 2, 2]
    })

    validator = Validator()

    assert validator.dq01_pk_uniqueness(
        df,
        "company_id"
    ) == 1