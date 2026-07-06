from src.screener.presets import *

from src.screener.export_excel import export_screeners


presets = {
    "Quality Compounder": quality_compounder(),
    "Value Pick": value_pick(),
    "Growth Accelerator": growth_accelerator(),
    "Dividend Champion": dividend_champion(),
    "Debt-Free Blue Chip": debt_free_bluechip(),
    "Turnaround Watch": turnaround_watch(),
}


for name, data in presets.items():

    print("=" * 60)
    print(name)
    print("=" * 60)

    print("Companies:", len(data))

    print(
        data[
            [
                "company_id",
                "year",
                "return_on_equity_pct",
                "debt_to_equity"
            ]
        ].head()
    )


# Export all presets to Excel
export_screeners(presets)

print("\n")
print("=" * 60)
print("screener_output.xlsx generated successfully")
print("=" * 60)