import sys
sys.path.append("src")
sys.path.append("src/hyperliq")

from hyperliquid.info import Info
from hyperliquid.utils import constants
from hyperliq_utils import hyperliquid_setup
import os
from dotenv import load_dotenv

load_dotenv()

from hyperliq.funding_rate import HyperliquidFundingRates

# Set up Hyperliquid client
hl_address, hl_info, hl_exchange = hyperliquid_setup(
    constants.MAINNET_API_URL, skip_ws=True
)


# info = Info(constants.MAINNET_API_URL, skip_ws=True)
# user_state = info.user_state(os.getenv("WALLET_ADDRESS"))
# print(float(user_state["withdrawable"]))


fr = HyperliquidFundingRates(
    hl_address, hl_info, hl_exchange
).get_hyperliquid_funding_rates()

print(fr)
