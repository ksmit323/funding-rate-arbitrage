import json
from eth_account import Account as EthAccount
from requests import Session
import requests

from account import Account
from config import Config
from order import Order
from pnl import PnL
from public import Public
from register import Register
from signer import Signer
# from position import Position


class Client(object):
    def __init__(
        self,
        config: Config,
        account: EthAccount,
    ) -> None:
        self._session = Session()
        self._config = config
        self._account = account

        self.signer = Signer()
        self.public = Public(config)
        self.register = Register(config, account)
        self.account = Account(config, self._session, self.signer, account)
        self.order = Order(config, self._session, self.signer, account)
        self.pnl = PnL(config, self._session, self.signer, account)
        # self.position = Position(config, self._session, self.signer, account)

        res = requests.get(
            "%s/v1/get_account?address=%s&broker_id=%s"
            % (self._config.base_url, account.address, self._config.broker_id)
        )
        response = json.loads(res.text)
        # print("get_account reponse:", response)

        if response["success"]:
            self._account_id: str = response["data"]["account_id"]
        else:
            self._account_id = self._register.register_account(account)

        self.signer._account_id = self._account_id

    def create_new_access_key(self):
        self.signer._key_pair = self.register.add_access_key()
