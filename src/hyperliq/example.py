from hyperliquid.info import Info
from hyperliquid.utils import constants
import os
from dotenv import load_dotenv
load_dotenv()


info = Info(constants.TESTNET_API_URL, skip_ws=True)
user_state = info.user_state(os.getenv("WALLET_ADDRESS"))
print(float(user_state["withdrawable"]))

