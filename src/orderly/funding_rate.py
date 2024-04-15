import requests


class FundingRate(object):
    def __init__(self):
        self.url = "https://testnet-api-evm.orderly.network/v1/public"

    def _get_data(self, url):
        response = requests.get(url)
        data = response.json()
        return data

    def get_funding_rate(self, symbol: str) -> int:
        url = self.url + f"/funding_rate/{symbol}"
        data = self._get_data(url)

        return data["data"]

    def get_all_funding_rates(self) -> list:
        # Minimum 24-hour volume threshold
        MIN_VOLUME = 100000

        url = self.url + "/futures"
        data = self._get_data(url)

        # Initialize list
        filtered_data = []

        # Check each entry for sufficient volume
        for entry in data["data"]["rows"]:
            if entry["24h_volume"] >= MIN_VOLUME:
                filtered_data.append((entry["symbol"], entry["est_funding_rate"]))

        return filtered_data

    def get_highest_funding_rate(self) -> tuple:
        funding_rates = self.get_all_funding_rates()

        highest_rate = None

        for symbol, rate in funding_rates:
            if highest_rate is None or rate > highest_rate[1]:
                highest_rate = (symbol, rate)

        return highest_rate


fr = FundingRate()
print(fr.get_all_funding_rates())