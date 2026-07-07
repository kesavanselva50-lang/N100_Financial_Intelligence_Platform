from src.portfolio.recommend import *


portfolios = {

    "Conservative": conservative_portfolio(),

    "Growth": growth_portfolio(),

    "Dividend": dividend_portfolio(),

    "Value": value_portfolio()

}


for name, df in portfolios.items():

    print("=" * 60)

    print(name)

    print("=" * 60)

    print(

        df[
            [
                "overall_rank",
                "company_id",
                "broad_sector",
                "composite_quality_score"
            ]
        ]

    )

    print()