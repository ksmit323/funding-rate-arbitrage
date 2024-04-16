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

# Need to get funding rates for each symbol


# # Usage
# orderly_rates = OrderlyFundingRates().get_orderly_funding_rates
# hyperliquid_rates = HyperliquidFundingRates().get_hyperliquid_funding_rates()

# perpArb = PerpToPerpArbitrage()

# perpArb.add_dex_rates("Orderly", orderly_rates)
# perpArb.add_dex_rates("Hyperlink", hyperliquid_rates)

# rates_table = perpArb.compile_rates()

# print(rates_table)


# # Usage
# orderly_rates = OrderlyFundingRates().get_orderly_funding_rates()
# hyperliquid_rates = HyperliquidFundingRates().get_hyperliquid_funding_rates()

# perpArb = PerpToPerpArbitrage()

# perpArb.add_dex_rates("Orderly", orderly_rates)
# perpArb.add_dex_rates("Hyperliquid", hyperliquid_rates)

# rates_table = perpArb.compile_rates()

# print(rates_table)


# if __name__ == "__main__":
#     main()

data = {'SEI': {'Orderly': 9.786e-05}, 'WOO': {'Orderly': 0.01108684}, 'DOGE': {'Orderly': 0.0001}, 'AVAX': {'Orderly': 0.0001, 'Hyperlink': 0.0001}, 'MATIC': {'Orderly': 0.0001, 'Hyperlink': 0.0001}, 'INJ': {'Orderly': 0.00132377, 'Hyperlink': 0.00048952}, 'ORDI': {'Orderly': 0.04, 'Hyperlink': 0.0001}, 'SUI': {'Orderly': 0.00029515, 'Hyperlink': 0.00050056}, 'SOL': {'Orderly': 0.00199359, 'Hyperlink': 0.00211304}, 'TIA': {'Orderly': 0.04, 'Hyperlink': 0.00078432}, 'JUP': {'Orderly': -0.0074358, 'Hyperlink': 0.0001}, 'WLD': {'Orderly': 0.00042325, 'Hyperlink': 0.0001}, 'WIF': {'Orderly': 0.00420913, 'Hyperlink': -0.00659176}, 'ARB': {'Orderly': 0.0001, 'Hyperlink': 0.0001}, 'ZEUS': {'Orderly': 0.0003471}, 'STRK': {'Orderly': 0.04}, 'LINK': {'Orderly': 0.00244583}, 'OP': {'Orderly': 0.00012613, 'Hyperlink': 0.0001}, 'BCH': {'Orderly': 0.0001}, 'APT': {'Hyperlink': 0.0004832}, 'ATOM': {'Hyperlink': 0.0001}, 'BTC': {'Hyperlink': 0.00242896}, 'ETH': {'Hyperlink': 0.00238576}, 'BNB': {'Hyperlink': -0.00063552}, 'GMT': {'Hyperlink': 0.0001}, 'DYDX': {'Hyperlink': 0.0001}, 'APE': {'Hyperlink': 0.0001}, 'kPEPE': {'Hyperlink': 0.0001}, 'RLB': {'Hyperlink': 0.0001}, 'HPOS': {'Hyperlink': 0.0001}, 'UNIBOT': {'Hyperlink': 0.0001}, 'COMP': {'Hyperlink': 0.0001}, 'FXS': {'Hyperlink': 0.0001}, 'MKR': {'Hyperlink': 0.0001}, 'AAVE': {'Hyperlink': 0.0001}, 'SNX': {'Hyperlink': 0.0001}, 'RNDR': {'Hyperlink': 0.0001}, 'LDO': {'Hyperlink': 0.0001}, 'STX': {'Hyperlink': 0.0001}, 'FTM': {'Hyperlink': 0.0001}, 'kSHIB': {'Hyperlink': 0.0001}, 'OX': {'Hyperlink': 0.02431616}, 'FRIEND': {'Hyperlink': 0.0001}, 'ZRO': {'Hyperlink': 0.0001}, 'BLZ': {'Hyperlink': 0.0001}, 'BANANA': {'Hyperlink': 0.0001}, 'FTT': {'Hyperlink': 0.0001}, 'TRB': {'Hyperlink': 0.0001}, 'CANTO': {'Hyperlink': 0.0001}, 'BIGTIME': {'Hyperlink': 0.0001}, 'NTRN': {'Hyperlink': 0.0001}, 'KAS': {'Hyperlink': 0.0001}, 'BLUR': {'Hyperlink': -0.00025528}, 'BSV': {'Hyperlink': 0.0001}, 'TON': {'Hyperlink': 0.10639096}, 'ADA': {'Hyperlink': 0.0001}, 'MINA': {'Hyperlink': 0.0001}, 'POLYX': {'Hyperlink': 0.0001}, 'GAS': {'Hyperlink': 0.0001}, 'AXL': {'Hyperlink': 0.0001}, 'PENDLE': {'Hyperlink': 0.07472984}, 'STG': {'Hyperlink': 0.0001}, 'FET': {'Hyperlink': 0.0001}, 'STRAX': {'Hyperlink': 0.32}, 'NEAR': {'Hyperlink': 0.0001}, 'MEME': {'Hyperlink': 0.0001}, 'BADGER': {'Hyperlink': 0.0001}, 'NEO': {'Hyperlink': -7.392e-05}, 'ZEN': {'Hyperlink': 0.0001}, 'FIL': {'Hyperlink': 0.0001}, 'PYTH': {'Hyperlink': 0.0001}, 'RUNE': {'Hyperlink': 0.0001}, 'SUSHI': {'Hyperlink': 0.0001}, 'ILV': {'Hyperlink': 0.0001}, 'MAV': {'Hyperlink': 0.0001}, 'IMX': {'Hyperlink': 0.0001}, 'kBONK': {'Hyperlink': 0.0001}, 'NFTI': {'Hyperlink': 0.0001}, 'SUPER': {'Hyperlink': -1.464e-05}, 'USTC': {'Hyperlink': 0.0001}, 'JOE': {'Hyperlink': 0.0001}, 'GALA': {'Hyperlink': 0.0001}, 'RSR': {'Hyperlink': 0.0001}, 'kLUNC': {'Hyperlink': 0.0001}, 'JTO': {'Hyperlink': 0.0001}, 'ACE': {'Hyperlink': 0.0001}, 'CAKE': {'Hyperlink': 0.0001}, 'PEOPLE': {'Hyperlink': 0.0001}, 'ENS': {'Hyperlink': 0.0001}, 'ETC': {'Hyperlink': 0.0001}, 'XAI': {'Hyperlink': 0.0001}, 'MANTA': {'Hyperlink': -9.456e-05}, 'UMA': {'Hyperlink': 0.0001}, 'REQ': {'Hyperlink': 0.0001}, 'ONDO': {'Hyperlink': 0.0001}, 'ALT': {'Hyperlink': 0.00184208}, 'ZETA': {'Hyperlink': 0.0001}, 'DYM': {'Hyperlink': 0.0001}, 'MAVIA': {'Hyperlink': 0.0001}, 'W': {'Hyperlink': 0.0001}, 'PANDORA': {'Hyperlink': 0.0001}, 'AI': {'Hyperlink': 0.0001}, 'TAO': {'Hyperlink': 0.00363504}, 'PIXEL': {'Hyperlink': 0.0001}, 'AR': {'Hyperlink': 0.0001}, 'TNSR': {'Hyperlink': 0.0001}}


df = pd.DataFrame(data).T
# Fill NaN values with a placeholder if any, such as 0 or 'n/a'
df.fillna(np.nan, inplace=True)
# Sort the DataFrame by index (symbol names) alphabetically
df.sort_index(inplace=True)
# Calculate the absolute difference
df["Difference"] = (df["Orderly"] - df["Hyperlink"]).abs()

# Print with tabulate for better formatting
print(tabulate(df, headers="keys", tablefmt="psql"))

# # Find the index of the max difference
# max_diff_index = df["Difference"].idxmax()

# # Print the row with the maximum difference
# max_diff_row = df.loc[max_diff_index]
# print(f"Row with the largest difference: \n{max_diff_row}")

# Get the top three rows with the largest differences
top_three_diff = df.nlargest(3, "Difference")
print("Top three rows with the largest differences:")
print(tabulate(top_three_diff, headers="keys", tablefmt="psql"))
