# Set Orderly Client
from base58 import b58decode
from eth_account import Account
from prompt_toolkit import HTML, print_formatted_text
import requests
from client import Client
from config import Config
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import os
import json
from requests import Request
from dotenv import load_dotenv

from order import Side

load_dotenv()

account: Account = Account.from_key(os.getenv("PRIVATE_KEY"))
config = Config()
client = Client(config, account)

# Set signer's Orderly key
key = b58decode(os.getenv("ORDERLY_SECRET_TESTNET"))
orderly_key = Ed25519PrivateKey.from_private_bytes(key)
client.signer._key_pair = orderly_key

# url = "https://testnet-api-evm.orderly.network/v1/position/PERP_ETH_USDC"
# url = "https://testnet-api-evm.orderly.network/v1/client/info"
# url = "https://testnet-api-evm.orderly.network/v1/client/statistics"
# url = "https://testnet-api-evm.orderly.network/v1/public/liquidated_positions"


# request = Request("GET", url)
# req = client.signer.sign_request(request)
# res = client._session.send(req)
# response = json.loads(res.text)
# print(response)

# print(client.order.create_market_order("ETH", 0.01, Side.BUY))
print(client.order.market_close_an_asset("TIA"))

# print(client.account.get_client_holding())

# url = f"https://testnet-api-evm.orderly.network/v1/public/futures/PERP_ETH_USDC"
# response = json.loads(requests.request("GET", url).text)
# print(response)
