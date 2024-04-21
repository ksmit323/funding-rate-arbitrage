from hyperliquid.utils import constants
import hyperliq.hyperliq_utils as hyperliq_utils
import time


class HyperliquidFundingRates(object):
    def __init__(self, address, info, exchange):
        """
        Parameters:
        address (str): The user's wallet address.
        info (object): An object to interact with Hyperliquid's API.
        exchange (object): An object representing the exchange.
        """
        self.address = address
        self.info = info
        self.exchange = exchange

    def get_funding_history(self, symbol: str) -> int:
        """
        Retrieves the funding history for a given symbol over the last 30 minutes.

        Parameters:
        symbol (str): The trading symbol for which funding history is to be retrieved (e.g. "BTC").

        Returns:
        int: The funding history for the specified symbol starting from 30 minutes ago.
        """
        # Current timestamp minus 30 mins to get the most recent fr
        start_time = int(time.time() * 1000) - 1800 * 1000

        return self.info.funding_history(symbol, start_time)

    def get_hyperliquid_funding_rates(self) -> dict:
        """
        Fetches asset names and their corresponding funding rates from the API.

        Returns:
        dict: a dictionary where the symbol is the key and the funding rate is the value
        """

        # Get meta data for all assets
        meta_data = hyperliq_utils.get_meta_data()

        # Separate the meta data into asset info and it's asset context
        asset_info = meta_data[0]["universe"]
        asset_context = meta_data[1]

        # Initialize dict to hold assets, funding rates
        assets_to_funding_rates = {}

        # Iterating over both lists, assuming they are aligned by index
        for asset, context in zip(asset_info, asset_context):
            symbol = asset["name"]
            funding_rate = (
                float(context["funding"]) * 8
            )  # convert to 8hr rate from 1hr rate
            assets_to_funding_rates[symbol] = funding_rate

        return assets_to_funding_rates
