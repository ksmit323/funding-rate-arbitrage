import json
from eth_account import Account
import requests

from config import Config


config = Config()
account = Account()

res = requests.post(
    "https://testnet-operator-evm.orderly.org/v1/faucet/usdc",
    headers={"Content-Type": "application/json"},
    json={
        "broker_id": config.broker_id,
        "chain_id": str(config.chain_id),
        "user_address": account.address,
    },
)
print(res.text)
response = json.loads(res.text)
print("USDC Faucet:", response)
