import json
import os

from eth_account import Account
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware

from orderly.client import Client
from orderly.config import Config
from orderly.order import OrderType, Side
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from base58 import b58decode

from dotenv import load_dotenv

load_dotenv()


# Set Client
account: Account = Account.from_key(os.getenv("PRIVATE_KEY"))
config = Config()
client = Client(config, account)

# Set signer's Orderly key
key = b58decode(os.getenv("ORDERLY_SECRET_TESTNET"))
orderly_key = Ed25519PrivateKey.from_private_bytes(key)
client.signer._key_pair = orderly_key

# symbols = client.public.get_symbols()
# print(symbols)

def main():
    ...

def get_holdings():
    holdings = client.account.get_client_holding()
    print(holdings)


def get_orders():
    orders = client.order.get_orders()
    print(orders)


# Intend on deleting this to reduce redundancy
def create_order(
    symbol: str,
    order_type: OrderType,
    order_quantity: float,
    side: Side,
):
    res = client.order.create_order(symbol, order_type, order_quantity, side)
    print("create_order:", res)


def cancel_all_orders():
    res = client.order.cancel_all_orders()
    print("Cancelled Orders: ", res)


def settle_pnl():
    res = client.pnl.settle_pnl()
    print("settle_pnl:", res)


# create_order("PERP_ETH_USDC", OrderType.MARKET, 0.01, Side.SELL)
# get_orders()

settle_pnl()

# Need to get funding rates for each symbol


if __name__ == "__main__":
    main()
