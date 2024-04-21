from enum import StrEnum
from hyperliquid.utils import constants
import hyperliq_utils as hyperliq_utils
import json


class Side(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class HyperLiquidOrder(object):
    def __init__(self):
        self.address, self.info, self.exchange = hyperliq_utils.setup(
            constants.TESTNET_API_URL, skip_ws=True
        )

    def create_market_order(
        self,
        symbol: str,
        order_quantity: float,
        side: Side,
    ):
        is_buy = True if str(side) == "BUY" else False
        order_result = self.exchange.market_open(
            symbol, is_buy, order_quantity, None, 0.01
        )

        if order_result["status"] == "ok":
            for status in order_result["response"]["data"]["statuses"]:
                try:
                    filled = status["filled"]
                except KeyError:
                    print(f'Error: {status["error"]}')
                    return order_result["status"]

        return order_result["status"]

    def create_limit_order(
        self, symbol: str, order_quantity: float, side: Side, limit_price: float
    ):

        is_buy = True if str(side) == "BUY" else False
        order_result = self.exchange.order(
            symbol, is_buy, order_quantity, limit_price, {"limit": {"tif": "Gtc"}}
        )
        print(order_result)

    def market_close_an_asset(self, symbol):
        order_result = self.exchange.market_close(symbol)

        if order_result["status"] == "ok":
            for status in order_result["response"]["data"]["statuses"]:
                try:
                    filled = status["filled"]
                    print(
                        f'Hyperliquid Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}'
                    )
                except KeyError:
                    print(f'Error: {status["error"]}')

    def cancel_open_orders(self):
        open_orders = self.info.open_orders(self.address)
        for open_order in open_orders:
            print(f"cancelling order {open_order}")
            self.exchange.cancel(open_order["coin"], open_order["oid"])

    def get_all_positions(self):
        """
        Get all Hyperliquid open positions

        returns: a list of dicts with symbols and position size
        """
        # Get the user state and print out position information
        user_state = self.info.user_state(self.address)
        filtered_positions = []
        for position in user_state["assetPositions"]:
            symbol = position["position"]["coin"]
            position_size = float(position["position"]["szi"])
            filtered_positions.append(
                {"symbol": symbol, "position_size": position_size}
            )

        if len(filtered_positions) == 0:
            return 0

        return filtered_positions



order = HyperLiquidOrder()
print(order.get_all_positions())
# order.create_market_order("ETH", 0.01, Side.SELL)
# order.market_close_one_asset("ETH")
# order.create_limit_order("PURR/USDC", 0.01, Side.BUY, 1000)
# order.cancel_open_orders()
