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
from strategies.funding_rate_arbitrage import FundingRateArbitrage
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from base58 import b58decode
from dotenv import load_dotenv

load_dotenv()


def prompt_user(options, prompt):
    """Helper function for CLI"""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}) {option} ")
    choice = int(input("Enter your choice: "))

    return choice


def orderly_get_holdings():
    print(client.account.get_client_holding())


def orderly_get_orders():
    print(client.order.get_orders())


def orderly_cancel_all_orders():
    res = client.order.cancel_all_orders()
    print("Cancelled Orders: ", res)
    return res


def orderly_settle_pnl():
    res = client.pnl.settle_pnl()
    print("settle_pnl:", res)
    return res


def analyze_funding_rate_arbitrage(option: int):

    # Initialize the strategy
    fr_arbitrage = FundingRateArbitrage()

    # Add data to the strategy
    for dex in DEX_rates_list:
        fr_arbitrage.add_dex_rates(dex[0], dex[1])

    # Create a data frame of the data
    compiled_rates = fr_arbitrage.compile_rates()
    df = fr_arbitrage.create_rates_table(compiled_rates)

    if option == 1:
        fr_arbitrage.display_rates_table(df)
    elif option == 2:
        fr_arbitrage.display_top_rates_differences_from_Orderly(df)
    else:
        fr_arbitrage.display_top_rates_differences_from_all_DEXs(df)


def create_order(dex, symbol, quantity, side):
    """Helper function to create an order on any DEX."""

    if dex == "orderly":
        response = client.order.create_market_order(
            symbol, quantity, side
        )
        print("\nOrderly Order:", response, "\n")
        return response["success"] == True

    elif dex == "hyperliquid":
        response = hyperliquid_order.create_market_order(symbol, quantity, side)
        return response == "ok"

    #* elif ADD DEX HERE


def execute_funding_rate_arbitrage(
    symbol: str, short_on_dex: str, long_on_dex: str, order_quantity: float
):
    """
    Short asset on DEX with the higher funding rate,
    long asset on DEX with the lower funding rate
    """
    # Execute short order
    if not create_order(short_on_dex, symbol, order_quantity, Side.SELL):
        print(f"{short_on_dex.title()} order failed, abort strategy")
        return

    # Execute long order
    if not create_order(long_on_dex, symbol, order_quantity, Side.BUY):
        print(f"{long_on_dex.title()} order failed, abort strategy")
        print("Close the short position!")
        # TODO: Consider adding logic to close the initial short order if needed
        return


# TODO: Add positons (view, close), add orders, add PnL, add margin, add PTSL


if __name__ == "__main__":

    # *** ADD DEX HERE ***:
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
    # *** ADD DEX HERE ***

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
                    "View top 3 rate differences from Orderly",
                    "View top 3 rate differences from all DEXs",
                    "Back to Main Menu",
                ]
                choice = prompt_user(options, "\nWhat would you like to do?")
                if choice >= 1 and choice <= 3:
                    analyze_funding_rate_arbitrage(choice)
                elif choice == 2:
                    analyze_funding_rate_arbitrage(2)
                elif choice == 3:
                    analyze_funding_rate_arbitrage(3)
                elif choice == 4:
                    break
                else:
                    print("\nInvalid choice, please try again!")
        elif choice == 7:
            options = ["Back to Main Menu"]
            ...
        elif choice == 8:
            # Put a note to the user to only put in the ticker symbol i.e. ETH
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
