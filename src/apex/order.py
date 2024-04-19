import os
import sys
import time
from apexpro.constants import APEX_HTTP_TEST, APEX_HTTP_MAIN
from apexpro.http_public import HttpPublic
from enum import StrEnum
from dotenv import load_dotenv
from apexpro.helpers.util import round_size
from apexpro.http_private_stark_key_sign import HttpPrivateStark
from apexpro.constants import (
    APEX_HTTP_TEST,
    NETWORKID_TEST,
)
from utils import get_apexpro_naming_convention

# Paths required by ApexPro API
root_path = os.path.abspath(__file__)
root_path = "/".join(root_path.split("/")[:-2])
sys.path.append(root_path)

load_dotenv()


class Side(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class ApexProOrder(object):
    def __init__(self):
        client = HttpPrivateStark(
            APEX_HTTP_TEST,
            network_id=NETWORKID_TEST,
            stark_public_key=os.getenv("STARK_PUBLIC_KEY"),
            stark_private_key=os.getenv("STARK_PRIVATE_KEY"),
            stark_public_key_y_coordinate=os.getenv("STARK_PUBLIC_KEY_Y_COORDINATE"),
            api_key_credentials={
                "key": os.getenv("APEX_API_KEY"),
                "secret": os.getenv("APEX_API_SECRET"),
                "passphrase": os.getenv("APEX_API_PASSPHRASE"),
            },
        )
        # Function calls required by ApexPro API
        self.configs = client.configs_v2()
        client.get_user()
        self.account = client.get_account_v2()
        self.client = client

    def create_order(
        self, symbol: str, side: Side, type: str, order_quantity: float, price: float
    ):
        """Helper function for creating orders"""
        currentTime = time.time()

        createOrderRes = self.client.create_order_v2(
            symbol=symbol,
            side=str(side),
            type=type,
            size=order_quantity,
            expirationEpochSeconds=currentTime,
            price=price,
            limitFeeRate="0.0005",
            timeInForce="POST_ONLY",
        )
        return createOrderRes

    def create_market_order(self, symbol: str, order_quantity: float, side: Side):
        apexpro_symbol = get_apexpro_naming_convention(symbol)

        # ApexPro API gets worse price from order books as the market price
        worstPrice = self.client.get_worst_price(
            symbol=apexpro_symbol, side=side, size=order_quantity
        )
        price = worstPrice["data"]["worstPrice"]

        createOrderRes = self.create_order(
            apexpro_symbol, side, "MARKET", order_quantity, price
        )

        return createOrderRes

    def create_limit_order(
        self, symbol: str, order_quantity: float, side: Side, limit_price: float
    ):
        apexpro_symbol = get_apexpro_naming_convention(symbol)

        createOrderRes = self.create_order(
            apexpro_symbol, side, "LIMIT", order_quantity, limit_price
        )
        return createOrderRes

    def market_close_an_asset(self, symbol):
        apexpro_symbol = get_apexpro_naming_convention(symbol)
        positions = self.account["data"]["positions"]

        for position in positions:
            if position["symbol"] == apexpro_symbol:
                side = position["side"]
                size = float(position["size"])
                if size != 0:
                    close_side = Side.BUY if side == "SHORT" else Side.SELL
                    createOrdeRes = self.create_market_order(symbol, size, close_side)

        return createOrdeRes

    def cancel_open_orders(self):
        print("Cancelling ApexPro open orders")
        return self.client.delete_open_orders()
