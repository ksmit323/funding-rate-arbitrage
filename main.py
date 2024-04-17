import os
import sys

sys.path.append("src")
sys.path.append("src/orderly")
sys.path.append("src/hyperliq")

from eth_account import Account
from hyperliq.funding_rate import HyperliquidFundingRates
from hyperliq.order import HyperLiquidOrder
from orderly.funding_rate import OrderlyFundingRates
from orderly.client import Client
from orderly.config import Config
from orderly.order import OrderType, Side
from strategies.perp_perp_arb import PerpToPerpArbitrage
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from base58 import b58decode
from dotenv import load_dotenv

load_dotenv()


def prompt_user(options, prompt):
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}) {option} ")
    choice = int(input("Enter your choice: "))

    return choice


def main_menu():

    while True:
        options = [
            "View open positions",  # 1
            "Close positions",  # 2
            "Cancel Open orders",  # 3
            "View PnL",  # 4
            "Settle Orderly PnL",  # 5
            "Analyze Perp-Perp Arbitrage Strategy",  # 6
            "Analyze Perp-Spot Arbitrage Strategy",  # 7
            "Execute Perp-Perp Arbitrage Strategy",  # 8
            "Execute Perp-Spot Arbitrage Strategy",  # 9
            "Exit",
        ]
        choice = prompt_user(options, "\nWhat would you like to do?")

        if choice == 1:
            ...
            options = ["Back to Main Menu"]
        elif choice == 2:
            ...
            options = ["Back to Main Menu"]

        elif choice == 3:
            ...
            options = ["Back to Main Menu"]

        elif choice == 4:
            ...
            options = ["Back to Main Menu"]

        elif choice == 5:
            options = ["Back to Main Menu"]
            ...
        elif choice == 6:
            while True:
                options = [
                    "View rates on all available DEXs",
                    "View top 3 rate differences on DEXs",
                    "Back to Main Menu",
                ]
                choice = prompt_user(options, "\nWhat would you like to do?")
                if choice == 1:
                    analyze_perp_perp_arbitrage(1)
                elif choice == 2:
                    analyze_perp_perp_arbitrage(2)
                elif choice == 3:
                    break
                else:
                    print("\nInvalid choice, please try again!")
        elif choice == 7:
            options = ["Back to Main Menu"]
            ...
        elif choice == 8:
            options = ["Back to Main Menu"]
            ...
        elif choice == 9:
            options = ["Back to Main Menu"]
            ...
        elif choice == 10:
            print("Exiting program, have a good day 😊")
            break
        else:
            print("Invalid choice, please try again")


def orderly_get_holdings():
    print(client.account.get_client_holding())


def orderly_get_orders():
    print(client.order.get_orders())


def orderly_create_order(
    symbol: str,
    order_type: OrderType,
    order_quantity: float,
    side: Side,
):
    res = client.order.create_order(symbol, order_type, order_quantity, side)
    print("create_order:", res)

    return res


def orderly_cancel_all_orders():
    res = client.order.cancel_all_orders()
    print("Cancelled Orders: ", res)

    return res


def orderly_settle_pnl():
    res = client.pnl.settle_pnl()
    print("settle_pnl:", res)

    return res


def analyze_perp_perp_arbitrage(option: int):

    # Initialize the strategy
    perpArb = PerpToPerpArbitrage()

    # Add data to the strategy
    for dex in DEX_rates_list:
        perpArb.add_dex_rates(dex[0], dex[1])

    # Create a data frame of the data
    compiled_rates = perpArb.compile_rates()
    df = perpArb.create_rates_table(compiled_rates)

    if option == 1:
        perpArb.display_rates_table(df)
    else:
        perpArb.display_top_rates_difference(df)


def execute_perp_perp_arbitrage(
    symbol: str, short_on_dex: str, long_on_dex: str, order_quantity: float
):
    """
    Short asset on DEX with the higher funding rate,
    long asset on DEX with the lower funding rate
    """
    orderly_symbol = "PERP_" + symbol + "_USDC"

    # Create short order on DEX
    if short_on_dex == "orderly":
        res = orderly_create_order(
            orderly_symbol, OrderType.MARKET, order_quantity, Side.SELL
        )
        if res["success"] != True:
            return print("Orderly order failed")

    elif short_on_dex == "hyperlink":
        order_status = hyperliquid_order.create_market_order(
            symbol, order_quantity, Side.SELL
        )
        if order_status != "ok":
            # TODO: Close Orderly position
            return print("Hyperliquid order failed, abort strategy")

    # Create long order on DEX
    if long_on_dex == "orderly":
        res = orderly_create_order(
            orderly_symbol, OrderType.MARKET, order_quantity, Side.BUY
        )
        if res["success"] != True:
            return print("Orderly order failed")
        
    elif long_on_dex == "hyperliquid":
        order_status = hyperliquid_order.create_market_order(
            symbol, order_quantity, Side.BUY
        )
        if order_status != "ok":
            # TODO: Close Orderly position
            return print("Hyperliquid order failed, abort strategy")


def analyze_perp_spot_arbitrage(): ...


def execute_perp_spot_arbitrage(): ...


# TODO: Add positons (view, close), add orders, add PnL, add margin, add PTSL


if __name__ == "__main__":

    # *** Add DEX rates here ***:
    DEX_rates_list = [
        ("orderly", OrderlyFundingRates().get_orderly_funding_rates()),
        ("hyperliquid", HyperliquidFundingRates().get_hyperliquid_funding_rates()),
    ]

    # Set Orderly Client
    account: Account = Account.from_key(os.getenv("PRIVATE_KEY"))
    config = Config()
    client = Client(config, account)

    # Set signer's Orderly key
    key = b58decode(os.getenv("ORDERLY_SECRET_TESTNET"))
    orderly_key = Ed25519PrivateKey.from_private_bytes(key)
    client.signer._key_pair = orderly_key

    # Initiate Hyperliquid Order object
    hyperliquid_order = HyperLiquidOrder()

    main_menu()
