from base58 import b58encode
import requests
import json
from eth_account import Account
from config import Config


def encode_key(key: bytes):
    return "ed25519:%s" % b58encode(key).decode("utf-8")


def get_brokers():
    url = "https://api-evm.orderly.org/v1/public/broker/name"
    response = requests.request("GET", url)

    return response.text


def get_faucet_USDC():

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
