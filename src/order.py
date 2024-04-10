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
    def __init__ (
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

    def get_orders(self):
        req = self._signer.sign_request(
            Request("GET", "%s/v1/orders" % self._config.base_url)
        )
        res = self._session.send(req)
        response = json.loads(res.text)
        return response

    def create_order(
        self,
        symbol:str,
        order_type: OrderType,
        order_quantity: float,
        side: Side,
    ):
        req = self._signer.sign_request(
            Request(
                "POST",
                "%s/v1/order" % self._config.base_url,
                json={
                    "symbol": symbol,
                    "order_type": str(order_type),
                    "order_quantity": order_quantity,
                    "side": str(side),
                },
            )
        )
        res = self._session.send(req)
        response = json.loads(res.text)
        return response
