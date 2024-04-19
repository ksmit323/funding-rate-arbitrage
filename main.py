import os
import sys

sys.path.append("src")
sys.path.append("src/orderly")
sys.path.append("src/hyperliq")
sys.path.append("src/apex")

import time
from eth_account import Account
from hyperliq.funding_rate import HyperliquidFundingRates
from hyperliq.order import HyperLiquidOrder
from orderly.funding_rate import OrderlyFundingRates
from orderly.client import Client
from orderly.config import Config
from orderly.order import OrderType, Side
from apex.funding_rate import ApexProFundingRates
from apex.order import ApexProOrder
from strategies.funding_rate_arbitrage import FundingRateArbitrage
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from base58 import b58decode
from dotenv import load_dotenv

from pyfiglet import Figlet
from prompt_toolkit import print_formatted_text, HTML


load_dotenv()


def prompt_user(options, prompt):
    """Helper function for CLI"""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}) {option} ")
    choice = int(input("Enter your choice: "))

    return choice


def clear_screen():
    """Helper function for CLI"""
    os.system("cls" if os.name == "nt" else "clear")


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
        response = client.order.create_market_order(symbol, quantity, side)
        success = response["success"] == True
        if success:
            print("Orderly order was successful")
        return success

    elif dex == "hyperliquid":
        response = hyperliquid_order.create_market_order(symbol, quantity, side)
        success = response == "ok"
        if success:
            print("Hyperliquid order was succesful")
        return success

    elif dex == "apexpro":
        response = apexpro_order.create_market_order(symbol, quantity, side)
        success = response["data"]["status"] == "PENDING"
        if success:
            print("ApexPro order was successful")
        return success

    # * elif ADD DEX HERE


def execute_funding_rate_arbitrage(
    symbol: str, short_on_dex: str, long_on_dex: str, order_quantity: float
):
    """
    Short asset on DEX with the higher funding rate,
    long asset on DEX with the lower funding rate
    """
    # Execute short order
    if not create_order(short_on_dex, symbol, order_quantity, Side.SELL):
        print(f"{short_on_dex.title()} order failed, aborting strategy")
        return False

    # Execute long order
    if not create_order(long_on_dex, symbol, order_quantity, Side.BUY):
        print(f"{long_on_dex.title()} order failed, aborting strategy")
        print("Closing the short position!")
        # TODO: Consider adding logic to close the initial short order if needed
        return False

    return True


# TODO: Add positons (view, close), add orders, add PnL, add margin, add PTSL


if __name__ == "__main__":

    # *** ADD DEX HERE ***:
    DEX_rates_list = [
        ("orderly", OrderlyFundingRates().get_orderly_funding_rates()),
        ("hyperliquid", HyperliquidFundingRates().get_hyperliquid_funding_rates()),
        ("apexpro", ApexProFundingRates().get_apexpro_funding_rates()),
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
    apexpro_order = ApexProOrder()
    # *** ADD DEX HERE ***

    figlet = Figlet()
    figlet.setFont(font="speed")

    while True:
        clear_screen()
        print(figlet.renderText("Funding Rate Arbitrage"))
        options = [
            "View open positions",  # 1
            "Close positions",  # 2
            "Cancel Open orders",  # 3
            "View PnL",  # 4
            "Start Funding Rate Strategy",  # 5
            "Exit",  # 6
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

            ...
        elif choice == 5:
            while True:
                options = [
                    "View rates on all available DEXs",
                    "View top 3 rate differences from Orderly",
                    "View top 3 rate differences from all DEXs",
                    "Execute Strategy",
                    "Back to Main Menu",
                ]
                choice = prompt_user(options, "\nWhat would you like to do?")
                if choice == 1:
                    clear_screen()
                    analyze_funding_rate_arbitrage(1)
                elif choice == 2:
                    clear_screen()
                    analyze_funding_rate_arbitrage(2)
                elif choice == 3:
                    clear_screen()
                    analyze_funding_rate_arbitrage(3)
                elif choice == 4:
                    print(
                        "\nWhen entering a symbol, just enter the symbol itself i.e. ETH\n"
                    )
                    symbol = input("Symbol to trade: ").upper()
                    dex_options = [
                        "orderly",
                        "hyperliquid",
                        "apexpro",
                    ]  # * Add any new DEXs to this list

                    # Prompt user to pick DEX to short on
                    choice = prompt_user(dex_options, "\nShort on what DEX?")
                    try:
                        short_on_dex = dex_options[choice - 1]
                    except IndexError:
                        print("Invalid choice, aborting!")

                    # Remove DEX from list of choices
                    del dex_options[choice - 1]

                    # Prompt user to pick DEX to long on
                    choice = prompt_user(dex_options, "\nLong on what DEX?")
                    try:
                        long_on_dex = dex_options[choice - 1]
                    except IndexError:
                        print("Invalid choice, aborting!")

                    # Prompt user for order quantity
                    order_quantity = float(input("\nEnter Order Quantity: "))

                    # Verify user's choices
                    print("\nYou chose to:")
                    print_formatted_text("Short on DEX: ", HTML(f"<ansired>{short_on_dex}</ansired>"))
                    print_formatted_text("Long on DEX: ", HTML(f"<ansigreen>{long_on_dex}</ansigreen>"))
                    print("Order Quantity: ", order_quantity)
                    options = ["Yes", "No"]
                    choice = prompt_user(options, "Are you sure this is correct?")
                    if choice == 1:
                        print("Okay! Let's Arbitrage!")
                    elif choice == 2:
                        print("Aborting!")
                        time.sleep(2)
                        break
                    else:
                        print("Invalid choice, aborting!")
                        time.sleep(2)
                        break

                    if execute_funding_rate_arbitrage(
                        symbol, short_on_dex, long_on_dex, order_quantity
                    ):
                        print(
                            "\nCongrats! You have succesfully performed the Funding Rate Arbitrage!"
                        )

                elif choice == 5:
                    clear_screen()
                    break
                else:
                    print("\nInvalid choice, please try again!")
                    time.sleep(1.5)
  
        elif choice == 5:
            print("\nExiting program, have a good day 😊\n")
            break
        else:
            print("\nInvalid choice, please try again")
            time.sleep(1.5)
