from eth_account import Account
import json
from requests import Request, Session
from config import Config
from signer import Signer
from order import Order


class Position(object):
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

    def get_one_position(self, symbol: str):
        """Get a position for a given symbol"""

    def get_all_positions(self):
        """Get all positions currently open"""

    def close_one_position(self, symbol: str):
        """Close a single position for a given asset"""

    def close_all_positions(self):
        """close all positions in the account"""