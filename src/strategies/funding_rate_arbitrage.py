import sys

sys.path.append("src")
sys.path.append("src/orderly")
sys.path.append("src/hyperliq")

import pandas as pd
import numpy as np
from tabulate import tabulate


class FundingRateArbitrage(object):
    def __init__(self):
        self.dex_rates = {}

    def add_dex_rates(self, dex_name: str, funding_rates: dict):
        """
        Adds a new set of funding rates for a specific DEX.

        Parameters:
        dex_name (str): The name of the DEX (e.g., "orderly").
        funding_rates (dict): A dictionary with asset symbols as keys and funding rates as values.
        """
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
        """
        Creates a Pandas DataFrame from compiled funding rates.

        Parameters:
        compiled_rates (dict): A dictionary of compiled funding rates, with asset symbols as keys
                               and DEX rates as values.

        Returns:
        pd.DataFrame: A DataFrame with symbols as the index and DEX names and rates as columns.
        """

        df = pd.DataFrame(compiled_rates).T

        # Fill NaN values with a nan
        df.fillna(np.nan, inplace=True)

        # Sort the DataFrame by index (symbol names) alphabetically
        df.sort_index(inplace=True)

        return df

    def display_rates_table(self, df):
        """
        Displays a table of funding rates for all assets on each DEX.

        Parameters:
        df (pd.DataFrame): A DataFrame containing compiled funding rates for each asset on various DEXs.
        """
        print("\nHere are the funding rates for all assets on each DEX:")
        print(tabulate(df, headers="keys", tablefmt="psql"))

    def display_top_rates_differences_from_all_DEXs(self, df):
        """
        Identifies and displays the top three assets with the largest funding rate differences
        among all DEXs.

        Parameters:
        df (pd.DataFrame): A DataFrame containing compiled funding rates for each asset on various DEXs.
        """
        # Calculate max/min while ignoring NaN
        df["MaxRate"] = df.max(axis=1, skipna=True)
        df["MinRate"] = df.min(axis=1, skipna=True)
        df["Difference"] = (df["MaxRate"] - df["MinRate"]).abs()

        # Get the top six rows with the largest differences
        top_diff = df.nlargest(6, "Difference")

        # print("\nTop three rows with the largest differences:")
        print(tabulate(top_diff, headers="keys", tablefmt="psql"))
