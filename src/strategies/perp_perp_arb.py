import sys

import pandas as pd
import numpy as np
from tabulate import tabulate


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
        all_rates = {}

        for dex_name, funding_rates in self.dex_rates.items():
            for symbol, rate in funding_rates.items():
                if symbol not in all_rates:
                    all_rates[symbol] = {}
                all_rates[symbol][dex_name] = rate

        return all_rates

    def create_rates_table(self, compiled_rates):

        df = pd.DataFrame(compiled_rates).T

        # Fill NaN values with a nan
        df.fillna(np.nan, inplace=True)

        # Sort the DataFrame by index (symbol names) alphabetically
        df.sort_index(inplace=True)

        return df

    def display_rates_table(self, df):
        print(tabulate(df, headers="keys", tablefmt="psql"))

    def display_top_rates_difference(self, df):

        # Calculate max/min while ignoring NaN
        df["MaxRate"] = df.max(axis=1, skipna=True)
        df["MinRate"] = df.min(axis=1, skipna=True)
        df["Difference"] = (df["MaxRate"] - df["MinRate"]).abs()

        # Get the top three rows with the largest differences
        top_three_diff = df.nlargest(3, "Difference")

        print("Top three rows with the largest differences:")
        print(tabulate(top_three_diff, headers="keys", tablefmt="psql"))












# # Usage
# orderly_rates = OrderlyFundingRates().get_orderly_funding_rates
# hyperliquid_rates = HyperliquidFundingRates().get_hyperliquid_funding_rates()

# perpArb = PerpToPerpArbitrage()

# perpArb.add_dex_rates("Orderly", orderly_rates)
# perpArb.add_dex_rates("Hyperlink", hyperliquid_rates)

# rates_table = perpArb.compile_rates()

# print(rates_table)
