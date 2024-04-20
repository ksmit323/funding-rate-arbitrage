from base58 import b58encode
from prompt_toolkit import HTML, print_formatted_text
import requests
import json
from eth_account import Account
from config import Config
from requests import Request


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

def get_orderly_naming_convention(symbol):
    return f"PERP_{symbol}_USDC"

def print_ascii_art():
    print_formatted_text(HTML("<ansigreen>███████╗██╗░░░██╗███╗░░██╗██████╗░██╗███╗░░██╗░██████╗░  ██████╗░░█████╗░████████╗███████╗</ansigreen>"))
    print_formatted_text(HTML("<ansigreen>██╔════╝██║░░░██║████╗░██║██╔══██╗██║████╗░██║██╔════╝░  ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝</ansigreen>"))
    print_formatted_text(HTML("<ansigreen>█████╗░░██║░░░██║██╔██╗██║██║░░██║██║██╔██╗██║██║░░██╗░  ██████╔╝███████║░░░██║░░░█████╗░░</ansigreen>"))
    print_formatted_text(HTML("<ansigreen>██╔══╝░░██║░░░██║██║╚████║██║░░██║██║██║╚████║██║░░╚██╗  ██╔══██╗██╔══██║░░░██║░░░██╔══╝░░</ansigreen>"))
    print_formatted_text(HTML("<ansigreen>██║░░░░░╚██████╔╝██║░╚███║██████╔╝██║██║░╚███║╚██████╔╝  ██║░░██║██║░░██║░░░██║░░░███████╗</ansigreen>"))
    print_formatted_text(HTML("<ansigreen>╚═╝░░░░░░╚═════╝░╚═╝░░╚══╝╚═════╝░╚═╝╚═╝░░╚══╝░╚═════╝░  ╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝</ansigreen>"))
    print("\n")
    print_formatted_text(HTML("<ansigreen>░█████╗░██████╗░██████╗░██╗████████╗██████╗░░█████╗░░██████╗░███████╗</ansigreen>"))
    print_formatted_text(HTML("<ansigreen>██╔══██╗██╔══██╗██╔══██╗██║╚══██╔══╝██╔══██╗██╔══██╗██╔════╝░██╔════╝</ansigreen>"))
    print_formatted_text(HTML("<ansigreen>███████║██████╔╝██████╦╝██║░░░██║░░░██████╔╝███████║██║░░██╗░█████╗░░</ansigreen>"))
    print_formatted_text(HTML("<ansigreen>██╔══██║██╔══██╗██╔══██╗██║░░░██║░░░██╔══██╗██╔══██║██║░░╚██╗██╔══╝░░</ansigreen>"))
    print_formatted_text(HTML("<ansigreen>██║░░██║██║░░██║██████╦╝██║░░░██║░░░██║░░██║██║░░██║╚██████╔╝███████╗</ansigreen>"))
    print_formatted_text(HTML("<ansigreen>╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░╚══════╝</ansigreen>"))