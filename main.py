import json
import os
import sys

sys.path.append("src")
sys.path.append("src/orderly")
sys.path.append("src/hyperliq")

from eth_account import Account
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware

from hyperliq.funding_rate import HyperliquidFundingRates
from orderly.funding_rate import OrderlyFundingRates
from orderly.client import Client
from orderly.config import Config
from orderly.order import OrderType, Side
from strategies.perp_perp_arb import PerpToPerpArbitrage
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from base58 import b58decode
from dotenv import load_dotenv

import pandas as pd
import numpy as np
from tabulate import tabulate

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



def perform_perp_perp_arbitrage():

    ## Usage

    # Get rates from each DEX
    orderly_rates = OrderlyFundingRates().get_orderly_funding_rates()
    hyperliquid_rates = HyperliquidFundingRates().get_hyperliquid_funding_rates()

    # Initialize the strategy
    perpArb = PerpToPerpArbitrage()

    # Add data to the strategy
    perpArb.add_dex_rates("Orderly", orderly_rates)
    perpArb.add_dex_rates("Hyperlink", hyperliquid_rates)

    # Create a data frame of the data
    compiled_rates = perpArb.compile_rates()
    df = perpArb.create_rates_table(compiled_rates)

    # Print the top differences in rates across each DEX
    perpArb.display_top_rates_difference(df)

    # Alternatively, print out all the rates for each asset on each DEX
    # perpArb.display_rates_table(df)


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

# Need to get funding rates for each symbol



if __name__ == "__main__":
    # Pick a strategy
    perform_perp_perp_arbitrage()

