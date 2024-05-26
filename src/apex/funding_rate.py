from apexpro.constants import APEX_WS_TEST
from apexpro.websocket_api import WebSocket
import time


class ApexProFundingRates(object):
    def __init__(self):
        self.ws_client = WebSocket(
            endpoint=APEX_WS_TEST,
        )

    def get_all_ticker_info(self):

        # function required by ApexPro WS API
        def h1(message):
            global all_ticker_info
            all_ticker_info = message

        self.ws_client.all_ticker_stream(h1)
        time.sleep(1)  # Wait for ws connection
        return all_ticker_info

    def get_apexpro_funding_rates(self):
        """
        Fetches asset names and their corresponding funding rates from the API.

        Returns:
        dict: a dictionary where the symbol is the key and the funding rate is the value
        """
        all_ticker_info = self.get_all_ticker_info()
        funding_rates = {}

        for entry in all_ticker_info["data"]:
            if "USDT" in entry["s"]:
                continue
            else:
                symbol = entry["s"].replace("USDC", "")
                funding_rates[symbol] = float(entry["fr"]) * 8 # Convert to 8hr funding rate

        return funding_rates
