import json
import os
import sys
import requests

sys.path.append("src")
sys.path.append("src/orderly")
sys.path.append("src/hyperliq")
sys.path.append("src/apex")

import time
from eth_account import Account
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from base58 import b58decode
from dotenv import load_dotenv
from hyperliq.hyperliq_utils import hyperliquid_setup
from hyperliq.funding_rate import HyperliquidFundingRates
from hyperliq.order import HyperLiquidOrder
from hyperliquid.utils import constants
from orderly.funding_rate import OrderlyFundingRates
from orderly.client import Client
from orderly.config import Config
from orderly.order import OrderType, Side
from orderly.util import print_ascii_art
from apex.funding_rate import ApexProFundingRates
from apex.order import ApexProOrder
from src.apex.apex_utils import apexpro_setup
from strategies.funding_rate_arbitrage import FundingRateArbitrage
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


def get_dex_from_dex_options(choice: int):
    try:
        return dex_options[choice - 1]
    except IndexError:
        print("Invalid choice, aborting!")


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


def market_close_an_asset(dex, symbol):
    """Helper function to market close an asset on any DEX."""

    if dex == "orderly":
        response = client.order.market_close_an_asset(symbol)
        success = response["success"] == True
        if success:
            print("Orderly order was successful")
        return success

    elif dex == "hyperliquid":
        response = hyperliquid_order.market_close_an_asset(symbol)
        success = response == "ok"
        if success:
            print("Hyperliquid order was successful")
        return success

    elif dex == "apexpro":
        response = apexpro_order.market_close_an_asset(symbol)
        success = response["data"]["status"] == "PENDING"
        if success:
            print("ApexPro order was successful")
        return success

    # * elif ADD NEW DEX HERE


def create_order(dex, symbol, quantity, side):
    """Helper function to create an order on any DEX."""

    if dex == "orderly":
        order_result = client.order.create_market_order(symbol, quantity, side)
        success = order_result["success"] == True

        # Workaround to get price as order_result['data']['order_price'] seems to only return None
        url = f"https://testnet-api-evm.orderly.network/v1/public/futures/PERP_{symbol}_USDC"
        response = json.loads(requests.request("GET", url).text)

        if success:
            print_formatted_text(
                f"Orderly order #{order_result['data']['order_id']} ",
                "filled ",
                HTML(
                    f"<ansigreen>{order_result['data']['order_quantity']}</ansigreen>"
                ),
                " at ",
                HTML(f"<ansigreen>{response['data']['mark_price']}</ansigreen>"),
            )
        return success

    elif dex == "hyperliquid":
        order_result = hyperliquid_order.create_market_order(symbol, quantity, side)
        success = order_result["status"] == "ok"
        if success:
            for status in order_result["response"]["data"]["statuses"]:
                try:
                    filled = status["filled"]
                    print_formatted_text(
                        f"Hyperliquid order #{filled['oid']} ",
                        "filled ",
                        HTML(f"<ansigreen>{filled['totalSz']}</ansigreen>"),
                        " at ",
                        HTML(f"<ansigreen>{filled['avgPx']}</ansigreen>"),
                    )

                except KeyError:
                    print(f'Error: {status["error"]}')
                    return order_result["status"]
        return success

    elif dex == "apexpro":
        order_result = apexpro_order.create_market_order(symbol, quantity, side)
        success = order_result["data"]["status"] == "PENDING"
        if success:
            print_formatted_text(
                f"ApexPro order #{order_result['data']['clientOrderId']} ",
                "filled ",
                HTML(f"<ansigreen>{order_result['data']['size']}</ansigreen>"),
                " at ",
                HTML(f"<ansigreen>{order_result['data']['price']}</ansigreen>"),
            )
        return success

    # * elif ADD NEW DEX HERE


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
        print("Close the short position!")
        # TODO: Consider adding logic to close the initial short order if needed
        return False

    return True


def print_open_positions(dex: str):
    # * ADD NEW DEX HERE
    if dex == "orderly":
        print("Orderly Positions: ")
        positions = client.order.get_all_positions()
    elif dex == "hyperliquid":
        print("Hyperliquid Positions: ")
        positions = hyperliquid_order.get_all_positions()
    elif dex == "apexpro":
        print("ApexPro Positions: ")
        positions = apexpro_order.get_all_positions()

    for position in positions:
        symbol = position["symbol"]
        size = position["position_size"]
        if size > 0:
            print_formatted_text(
                f"     {symbol}: ", HTML(f"<ansigreen>{size}</ansigreen>")
            )
        else:
            print_formatted_text(f"     {symbol}: ", HTML(f"<ansired>{size}</ansired>"))


def print_available_USDC_per_DEX(dex: str, usdc_amount: float):
    print(dex + ":")
    print_formatted_text(HTML(f"<ansigreen>{usdc_amount} USDC</ansigreen>"))


def cancel_open_orders(dex: str):
    if dex == "orderly":
        client.order.cancel_all_orders()
    elif dex == "hyperliquid":
        hyperliquid_order.cancel_open_orders()
    elif dex == "apexpro":
        apexpro_order.cancel_open_orders()


if __name__ == "__main__":

    # Set Orderly Client
    account: Account = Account.from_key(os.getenv("PRIVATE_KEY"))
    config = Config()
    client = Client(config, account)

    # Set signer's Orderly key
    key = b58decode(os.getenv("ORDERLY_SECRET_TESTNET"))
    orderly_key = Ed25519PrivateKey.from_private_bytes(key)
    client.signer._key_pair = orderly_key

    # Set up Hyperliquid client
    hl_address, hl_info, hl_exchange = hyperliquid_setup(
        constants.TESTNET_API_URL, skip_ws=True
    )

    # Set up ApexPro client
    apexpro_client = apexpro_setup()

    # Initiate DEX Order object
    hyperliquid_order = HyperLiquidOrder(hl_address, hl_info, hl_exchange)
    apexpro_order = ApexProOrder(apexpro_client)
    # *** ADD NEW DEX HERE ***

    DEX_rates_list = [
        ("orderly", OrderlyFundingRates().get_orderly_funding_rates()),
        (
            "hyperliquid",
            HyperliquidFundingRates(
                hl_address, hl_info, hl_exchange
            ).get_hyperliquid_funding_rates(),
        ),
        ("apexpro", ApexProFundingRates().get_apexpro_funding_rates()),
        # *** ADD NEW DEX HERE ***:
    ]

    while True:
        clear_screen()
        print_ascii_art()

        # *** ADD NEW DEX HERE ***:
        dex_options = [
            "orderly",
            "hyperliquid",
            "apexpro",
        ]
        options = [
            "View USDC balances on each DEX",  # 1
            "View open positions",  # 2
            "Close positions",  # 3
            "Cancel Open orders",  # 4
            "Start Funding Rate Strategy",  # 5
            "Exit",  # 6
        ]
        choice = prompt_user(options, "\nWhat would you like to do?")

        if choice == 1:
            print("\n")
            orderly_amount = float(client.account.get_client_holding()[0]["holding"])
            print_available_USDC_per_DEX("Orderly balance", orderly_amount)
            hyperliquid_amount = float(hl_info.user_state(hl_address)["withdrawable"])
            print_available_USDC_per_DEX("Hyperliquid balance", hyperliquid_amount)
            apexpro_amount = float(
                apexpro_order.account["data"]["wallets"][0]["balance"]
            )
            print_available_USDC_per_DEX("ApexPro balance", apexpro_amount)
            options = ["Back to Main Menu"]
            choice = prompt_user(options, "")
            if choice:
                continue

        if choice == 2:
            print("\n")
            for dex in dex_options:
                print_open_positions(dex)
            options = ["Back to Main Menu"]
            choice = prompt_user(options, "")
            if choice:
                continue

        elif choice == 3:

            # Prompt user for DEX
            choice = prompt_user(
                dex_options, "\nWhat DEX would you like to close positions on?"
            )
            close_on_dex = get_dex_from_dex_options(choice)

            # Prompt user for symbol
            print("\nWhen entering a symbol, just enter the symbol itself i.e. ETH\n")
            symbol = input("Symbol to close: ").upper()

            # Close position depending on DEX
            success = market_close_an_asset(close_on_dex, symbol)
            if success:
                print_formatted_text(
                    HTML(f"<ansigreen>{symbol}</ansigreen>"),
                    "has been closed on",
                    HTML(f"<ansigreen>{close_on_dex}</ansigreen>"),
                )
                options = ["Back to the Main Menu", "Exit Program"]
                choice = prompt_user(options, "\nWhat would you like to do?")
                if choice == 1:
                    continue
                else:
                    print("\nExiting program, have a good day 😊\n")
                    break

            else:
                print("Order has failed!")
                time.sleep(2)

        elif choice == 4:
            dex_options.append("Back to Main Menu")

            while True:
                choice = prompt_user(
                    dex_options, "\nWhat DEX would you like to close open orders on?"
                )
                # User chose back to main menu
                if choice == len(dex_options):
                    break

                # Cancel orders on selected DEX
                dex = get_dex_from_dex_options(choice)
                cancel_open_orders(dex)
                print_formatted_text(
                    "Open positions have been closed on",
                    HTML(f"<ansigreen>{dex}</ansigreen>"),
                )
                # Remove DEX from list of choices
                del dex_options[choice - 1]

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

                    # Prompt user for symbol
                    print(
                        "\nWhen entering a symbol, just enter the symbol itself i.e. ETH\n"
                    )
                    symbol = input("Symbol to trade: ").upper()

                    # Prompt user to pick DEX to short on
                    choice = prompt_user(dex_options, "\nShort on what DEX?")
                    short_on_dex = get_dex_from_dex_options(choice)

                    # Remove DEX from list of choices
                    del dex_options[choice - 1]

                    # Prompt user to pick DEX to long on
                    choice = prompt_user(dex_options, "\nLong on what DEX?")
                    long_on_dex = get_dex_from_dex_options(choice)

                    # Prompt user for order quantity
                    order_quantity = float(input("\nEnter Order Quantity: "))

                    # Verify user's choices
                    print("\nYou chose to:")
                    print_formatted_text(
                        "Short on DEX: ", HTML(f"<ansired>{short_on_dex}</ansired>")
                    )
                    print_formatted_text(
                        "Long on DEX: ", HTML(f"<ansigreen>{long_on_dex}</ansigreen>")
                    )
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
                        print_formatted_text(
                            HTML(
                                "<ansiblue>\nCongrats!🥳 You have succesfully performed the Funding Rate Arbitrage!</ansiblue>"
                            )
                        )

                elif choice == 5:
                    break
                else:
                    print("\nInvalid choice, please try again!")
                    time.sleep(1.5)

        elif choice == 6:
            print("\nExiting program, have a good day 😊\n")
            break
        else:
            print("\nInvalid choice, please try again")
            time.sleep(1.5)
