import pandas as pd

file = "data/raw/companies.xlsx"

df = pd.read_excel(file, header=None)

print(df.head(10))