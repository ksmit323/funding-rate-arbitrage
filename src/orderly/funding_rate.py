import requests


class OrderlyFundingRates(object):
    def __init__(self):
        self.url = "https://testnet-api-evm.orderly.network/v1/public"

    def _get_data(self, url):
        """
        Parameters:
        url (str): The API endpoint to send the request to.

        Returns:
        dict: The JSON response from the API, converted to a dictionary.
        """
        response = requests.get(url)
        data = response.json()
        return data

    def get_funding_rate(self, symbol: str) -> int:
        """
        Retrieves the funding rate for a given symbol from the Orderly Network API.

        Parameters:
        symbol (str): The trading symbol for which the funding rate is to be retrieved (e.g., "BTC-USDC").

        Returns:
        int: The funding rate for the specified symbol.
        """
        url = self.url + f"/funding_rate/{symbol}"
        data = self._get_data(url)

        return data["data"]

    def get_orderly_funding_rates(self) -> dict:
        """
        Fetches funding rates for all symbols with at least a 24-hour volume threshold.

        This function retrieves all funding rates from the Orderly Network API and filters them by a minimum
        24-hour volume to ensure sufficient liquidity.

        Returns:
        dict: A dictionary where the keys are asset symbols, and the values are their estimated funding rates.
        """
        # Minimum 24-hour volume threshold in monetary value, not trades!
        MIN_VOLUME = 100000

        url = self.url + "/futures"
        data = self._get_data(url)

        # Initialize dict
        filtered_data = {}

        # Check each entry for sufficient volume
        for entry in data["data"]["rows"]:
            if entry["24h_amount"] >= MIN_VOLUME:
                symbol = entry["symbol"].replace("PERP_", "").replace("_USDC", "") # Extract out just the ticker
                filtered_data[symbol] = entry["est_funding_rate"]

        return filtered_data

    def get_highest_funding_rate(self) -> tuple:
        """
        Retrieves the symbol with the highest funding rate from Orderly Network.

        Returns:
        tuple: A tuple containing the symbol with the highest funding rate and the corresponding rate.
        """
        funding_rates = self.get_all_funding_rates()

        highest_rate = None

        for symbol, rate in funding_rates:
            if highest_rate is None or rate > highest_rate[1]:
                highest_rate = (symbol, rate)

        return highest_rate
