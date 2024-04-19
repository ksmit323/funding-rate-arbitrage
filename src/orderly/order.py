from enum import StrEnum
from eth_account import Account
import json
from requests import Request, Session
from config import Config
from signer import Signer


class Side(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(StrEnum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class Order(object):
    def __init__(
        self,
        config: Config,
        session: Session,
        signer: Signer,
        account: Account,
    ) -> None:
        self._config = config
        self._session = session
        self._signer = signer
        self._account = account

    def _send_request(self, request: Request):
        """Helper function"""
        req = self._signer.sign_request(request)
        res = self._session.send(req)
        response = json.loads(res.text)
        return response

    def get_orders(self):
        request = Request("GET", "%s/v1/orders" % self._config.base_url)
        return self._send_request(request)

    def create_market_order(
        self,
        symbol: str,
        order_quantity: float,
        side: Side,
    ):
        symbol = f"PERP_{symbol}_USDC"

        # TODO: Need to add more to the JSON for limit orders
        request = Request(
            "POST",
            "%s/v1/order" % self._config.base_url,
            json={
                "symbol": symbol,
                "order_type": str(OrderType.MARKET),
                "order_quantity": order_quantity,
                "side": str(side),
            },
        )
        return self._send_request(request)

    # TODO: Create limit order
    def create_limit_order(
        self,
        symbol: str,
        order_quantity: float,
        side: Side,
    ): ...

    # TODO: Market close an asset
    def market_close_an_asset(self, symbol): ...

    def cancel_all_orders(self):
        request = Request(
            "DELETE",
            "%s/v1/orders"
            % self._config.base_url,  # Be careful, orders has to be plural here
        )
        return self._send_request(request)
