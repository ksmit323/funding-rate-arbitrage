import time
from enum import StrEnum
from dotenv import load_dotenv
from apex_utils import get_apexpro_naming_convention

load_dotenv()


class Side(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class ApexProOrder(object):
    def __init__(self, client):
        """
        Parameters:
        client (Client): A client object used to interact with the ApexPro API.
        """
        self.client = client

        # Function calls required by ApexPro API
        self.configs = client.configs_v2()
        client.get_user()
        self.account = client.get_account_v2()

    def create_order(
        self, symbol: str, side: Side, type: str, order_quantity: float, price: float
    ):
        """
        Helper function for creating orders"

        Parameters:
        symbol (str): The trading symbol for the order (e.g., "BTC").
        side (Side): The order side, either BUY or SELL.
        type (str): The order type, such as "LIMIT" or "MARKET".
        order_quantity (float): The quantity of the asset to be ordered.
        price (float): The price for the order.

        Returns:
        dict: The response from the ApexPro API after creating the order.
        """
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
        """
        Creates a market order on ApexPro.

        Parameters:
        symbol (str): The trading symbol for the order (e.g., "BTC-USDC").
        order_quantity (float): The quantity of the asset to be ordered.
        side (Side): The order side, either BUY or SELL.

        Returns:
        dict: The response from the ApexPro API after creating the market order.
        """
        apexpro_symbol = get_apexpro_naming_convention(symbol)

        # ApexPro API gets worse price from order books as the market price
        worstPrice = self.client.get_worst_price(
            symbol=apexpro_symbol, side=side, size=order_quantity
        )
        price = worstPrice["data"]["worstPrice"]

        return self.create_order(apexpro_symbol, side, "MARKET", order_quantity, price)

    def create_limit_order(
        self, symbol: str, order_quantity: float, side: Side, limit_price: float
    ):
        """
        Creates a limit order on ApexPro.

        Parameters:
        symbol (str): The trading symbol for the order (e.g., "BTC").
        order_quantity (float): The quantity of the asset to be ordered.
        side (Side): The order side, either BUY or SELL.
        limit_price (float): The limit price for the order.

        Returns:
        dict: The response from the ApexPro API after creating the limit order.
        """
        apexpro_symbol = get_apexpro_naming_convention(symbol)

        createOrderRes = self.create_order(
            apexpro_symbol, side, "LIMIT", order_quantity, limit_price
        )
        return createOrderRes

    def market_close_an_asset(self, symbol):
        """
        Closes an open position in the market for a given asset.

        Parameters:
        symbol (str): The trading symbol of the asset to close (e.g., "BTC").

        Returns:
        dict: The response from the ApexPro API after creating the market close order.
        """
        # Convert
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
        """
        Cancels all open orders on ApexPro.

        Returns:
        dict: The response from the ApexPro API after cancelling open orders.
        """
        return self.client.delete_open_orders()

    def get_all_positions(self):
        """
        Retrieves all open positions from the account and filters out those with a size of zero.

        Returns:
        list or int: A list of positions with non-zero sizes, with shorts represented as negative values. 
                     Returns 0 if no non-zero positions are found.
        """
        positions = self.account["data"]["positions"]

        filtered_positions = []

        for position in positions:
            symbol = position["symbol"].replace("-USDC", "")
            position_size = float(position["size"])
            if position_size != 0:
                # Flip position negative for shorts
                if position["side"] == "SHORT":
                    position_size = position_size * -1
                filtered_positions.append(
                    {"symbol": symbol, "position_size": position_size}
                )

        if len(filtered_positions) == 0:
            print("     No open positions")

        return filtered_positions
