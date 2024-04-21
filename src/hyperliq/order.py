from enum import StrEnum
from hyperliquid.utils import constants
import hyperliq_utils as hyperliq_utils
import json


class Side(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class HyperLiquidOrder(object):
    def __init__(self, address, info, exchange):
        """
        Parameters:
        address (str): The user's wallet address on the Hyperliquid platform.
        info (object): An object to interact with Hyperliquid's API.
        exchange (object): An object representing the exchange for order-related operations.
        """
        self.address = address
        self.info = info
        self.exchange = exchange

    def create_market_order(
        self,
        symbol: str,
        order_quantity: float,
        side: Side,
    ):
        """
        Creates a market order on Hyperliquid.

        Parameters:
        symbol (str): The trading symbol for the order (e.g., "BTC-USD").
        order_quantity (float): The quantity of the asset to be ordered.
        side (Side): The order side, either BUY or SELL.

        Returns:
        dict: The response from the Hyperliquid platform after creating the market order.
        """
        is_buy = True if str(side) == "BUY" else False
        order_result = self.exchange.market_open(
            symbol, is_buy, order_quantity, None, 0.01
        )

        # if order_result["status"] == "ok":
        #     for status in order_result["response"]["data"]["statuses"]:
        #         try:
        #             filled = status["filled"]
        #             print(
        #                 f'Hyperliquid Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}'
        #             )
        #         except KeyError:
        #             print(f'Error: {status["error"]}')
        #             return order_result["status"]
        return order_result

        return order_result["status"]

    def create_limit_order(
        self, symbol: str, order_quantity: float, side: Side, limit_price: float
    ):
        """
        Creates a limit order on Hyperliquid.

        Parameters:
        symbol (str): The trading symbol for the order (e.g., "BTC-USD").
        order_quantity (float): The quantity of the asset to be ordered.
        side (Side): The order side, either BUY or SELL.
        limit_price (float): The limit price for the order.

        Returns:
        dict: The response from the Hyperliquid platform after creating the limit order.
        """

        is_buy = True if str(side) == "BUY" else False
        order_result = self.exchange.order(
            symbol, is_buy, order_quantity, limit_price, {"limit": {"tif": "Gtc"}}
        )
        print(order_result)

    def market_close_an_asset(self, symbol):
        """
        Closes an open market position for a given asset on Hyperliquid.

        Parameters:
        symbol (str): The trading symbol of the asset to be closed (e.g., "BTC-USD").
        """
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
            if position_size != 0:
                filtered_positions.append(
                    {"symbol": symbol, "position_size": position_size}
                )

        if len(filtered_positions) == 0:
            return 0

        return filtered_positions
