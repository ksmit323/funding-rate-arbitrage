import sys

sys.path.append("src")
sys.path.append("src/orderly")
sys.path.append("src/hyperliq")

import pandas as pd
import numpy as np
from tabulate import tabulate

from funding_rate import OrderlyFundingRates
from hyperliq.funding_rate import HyperliquidFundingRates


class PerpToPerpArbitrage(object):
    def __init__(self):
        self.dex_rates = {}

    def add_dex_rates(self, dex_name: str, funding_rates: dict):
        """Adds a new set of rates for a given DEX"""
        self.dex_rates[dex_name] = funding_rates

    def compile_rates(self):
        """
        Compiles funding rates from all DEXs that were added with the add_dex_rates function

        Returns:
        dict: A dictionary where keys are symbols and values are dictionaries of DEX names and rates.
        """
        compiled_rates = {}

        for dex_name, funding_rates in self.dex_rates.items():
            for symbol, rate in funding_rates.items():
                if symbol not in compiled_rates:
                    compiled_rates[symbol] = {}
                compiled_rates[symbol][dex_name] = rate

        return compiled_rates

    def create_rates_table(self, compiled_rates):

        df = pd.DataFrame(compiled_rates).T

        # Fill NaN values with a nan
        df.fillna(np.nan, inplace=True)

        # Sort the DataFrame by index (symbol names) alphabetically
        df.sort_index(inplace=True)

        return df

    def display_rates_table(self, df):
        print("\nHere are the funding rates for all assets on each DEX:")
        print(tabulate(df, headers="keys", tablefmt="psql"))

    def display_top_rates_differences_from_Orderly(self, df):

        def max_diff_and_dex(row):
            """Function to calculate the maximum difference from Orderly and identify the DEX"""
            orderly_rate = row["Orderly"]
            max_diff = 0
            max_dex = None
            for dex, rate in row.items():
                if dex != "Orderly":
                    diff = abs(orderly_rate - rate)
                    if diff > max_diff:
                        max_diff = diff
                        max_dex = dex
            return pd.Series([max_diff, max_dex], index=["MaxDiff", "MaxDEX"])

        # Apply the function to each row and create new columns for the difference and the corresponding DEX
        df[["Max Orderly Diff", "DEX with Max Diff"]] = df.apply(
            max_diff_and_dex, axis=1
        )

        # Get the top three rows with the largest differences
        top_three_diff = df.nlargest(3, "Max Orderly Diff")

        # print("\nTop three rows with the largest differences:")
        print(tabulate(top_three_diff, headers="keys", tablefmt="psql"))

    def display_top_rates_differences_from_all_DEXs(self, df):

        # Calculate max/min while ignoring NaN
        df["MaxRate"] = df.max(axis=1, skipna=True)
        df["MinRate"] = df.min(axis=1, skipna=True)
        df["Difference"] = (df["MaxRate"] - df["MinRate"]).abs()

        # Get the top three rows with the largest differences
        top_three_diff = df.nlargest(3, "Difference")

        # print("\nTop three rows with the largest differences:")
        print(tabulate(top_three_diff, headers="keys", tablefmt="psql"))


# # Usage
orderly_rates = OrderlyFundingRates().get_orderly_funding_rates()
hyperliquid_rates = HyperliquidFundingRates().get_hyperliquid_funding_rates()

perpArb = PerpToPerpArbitrage()

perpArb.add_dex_rates("Orderly", orderly_rates)
perpArb.add_dex_rates("Hyperlink", hyperliquid_rates)

compiled_rates = perpArb.compile_rates()
df = perpArb.create_rates_table(compiled_rates)

perpArb.display_top_rates_differences_from_Orderly(df)
