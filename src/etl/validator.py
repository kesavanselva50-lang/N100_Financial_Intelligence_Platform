"""
Data Quality Validator
"""

import pandas as pd


class Validator:

    def dq01_pk_uniqueness(self, df, column):
        return df[column].duplicated().sum()

    def dq02_company_year_pk(self, df):
        return df.duplicated(
            subset=["company_id", "year"]
        ).sum()

    def dq03_fk_integrity(
        self,
        child_df,
        parent_df,
        fk_col,
        pk_col
    ):
        invalid = ~child_df[fk_col].isin(
            parent_df[pk_col]
        )
        return invalid.sum()

    def dq04_balance_sheet(self, df):
        return (
            abs(
                df["total_assets"]
                - df["total_liabilities"]
            ) > 1
        ).sum()

    def dq05_opm_check(self, df):

        calculated = (
            df["operating_profit"]
            / df["sales"]
            * 100
        )

        return (
            abs(
                calculated
                - df["opm_percentage"]
            ) > 1
        ).sum()

    def dq06_positive_sales(self, df):

        if "sales" not in df.columns:
            return 0

        return (
            df["sales"] <= 0
        ).sum()