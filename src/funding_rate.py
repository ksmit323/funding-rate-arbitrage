from eth_account import Account
import json
from requests import Request, Session
from config import Config
from signer import Signer
import requests


class FundingRate(object):
    def __init__(self):
        self.url = "https://testnet-api-evm.orderly.network/v1/public"

    def get_funding_rate(self, symbol: str) -> int:

        url = self.url + f"/funding_rate/{symbol}"
        
        response = requests.request("GET", url)
        json = response.json()

        return json["data"]

    def get_all_funding_rates(self) -> list:

        url = self.url + "/funding_rates"

        response = requests.request("GET", url)
        json = response.json()

        return json["data"]["rows"]
    


    




fr = FundingRate()

print(fr.get_funding_rate("PERP_ETH_USDC"))

# print(fr.get_all_est_funding_rates())
