from dotenv import load_dotenv
import json
import os

from eth_account import Account
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware

from client import Client
from config import Config
from order import OrderType, Side

load_dotenv()

account: Account = Account.from_key(os.getenv("PRIVATE_KEY"))

print("Address: ", account.address)

config = Config()
