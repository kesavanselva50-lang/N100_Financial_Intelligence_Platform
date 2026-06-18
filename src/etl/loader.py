import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")


def load_excel(filename):
    filepath = DATA_DIR / filename

    return pd.read_excel(
        filepath,
        header=1
    )


if __name__ == "__main__":

    companies = load_excel("companies.xlsx")

    print(companies.head())
    print("\nColumns:")
    print(companies.columns.tolist())