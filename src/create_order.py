from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime
import requests
import json
from base58 import b58decode
from requests import Request, Session

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from signer import Signer

# def create_order_example():

#     testnet_url = os.getenv("ORDERLY_TESTNET_URL")
#     orderly_account_id = os.getenv("ORDERLY_ACCOUNT_ID")

#     key = b58decode(os.environ.get("ORDERLY_SECRET_TESTNET"))

#     orderly_key = Ed25519PrivateKey.from_private_bytes(key)

#     session = Session()
#     signer = Signer(orderly_account_id, orderly_key)

#     req = signer.sign_request(
#         Request(
#             "POST",
#             "%s/v1/order" % testnet_url,
#             json={
#                 "symbol": "PERP_ETH_USDC",
#                 "order_type": "MARKET",
#                 "order_quantity": 0.01,
#                 "side": "BUY",
#             },
#         )
#     )
#     res = session.send(req)
#     response = json.loads(res.text)

#     print(response.text)

# create_order_example()

def create_order():
    wallet_address = os.getenv("WALLET_ADDRESS")

    time_in_ms = int(datetime.now().timestamp() * 1000)

    key = os.getenv("ORDERLY_KEY_TESTNET")
    secret = os.getenv("ORDERLY_SECRET_TESTNET")
    account = os.getenv("ACCOUNT_ID")

    url = os.getenv("ORDERLY_TESTNET_URL")

    payload = {
        "symbol": "PERP_WOO_USDC",
        # "client_order_id": "<string>",
        "order_type": "MARKET",
        # "order_price": 123,
        # "order_quantity": 123,
        "order_amount": 1,
        # "visible_quantity": 123,
        "side": "BUY",
        "reduce_only": True,
        "slippage": 123,
        # "order_tag": "<string>",
    }

    headers = {
        "orderly-timestamp": str(time_in_ms),
        "orderly-account-id": account,
        "orderly-key": key,
        "orderly-signature": secret,
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)






create_order()
