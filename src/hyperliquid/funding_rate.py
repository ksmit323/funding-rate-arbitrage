from hyperliquid.utils import constants
import utils
import time


class FundingRate(object):
    def __init__(self):
        self.address, self.info, self.exchange = utils.setup(
            constants.TESTNET_API_URL, skip_ws=True
        )

    def get_funding_history(self, symbol: str) -> int:

        # Current timestamp minus 30 mins to get the most recent fr
        timestamp = int(time.time() * 1000) - 1800 * 1000

        return self.info.funding_history(symbol, timestamp)

    def get_hyperliquid_funding_rates(self):
        """
        Fetches asset names and their corresponding funding rates from the API.

        Returns:
        list of tuples: A list containing tuples of (asset name, funding rate).
        """

        # Get meta data for all assets
        meta_data = utils.get_meta_data()

        # Separate the meta data into asset info and it's asset context
        asset_info = meta_data[0]["universe"]
        asset_context = meta_data[1]

        # Initialize list to hold assets, funding rates
        assets_and_funding_rates = []

        # Iterating over both lists, assuming they are aligned by index
        for asset, context in zip(asset_info, asset_context):
            name = asset["name"]
            funding_rate = float(context["funding"]) * 8 # convert to 8hr rate from 1hr rate
            assets_and_funding_rates.append((name, funding_rate))

        return assets_and_funding_rates


fr = FundingRate()

# fr.get_funding_history()
print(fr.get_hyperliquid_funding_rates())
