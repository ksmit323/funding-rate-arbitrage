from eth_account import Account
import json
from requests import Request, Session
from config import Config
from signer import Signer
from order import Order
from util import (
    get_orderly_naming_convention,
    get_position_request,
    get_all_positions_request,
)   


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

    #TODO: Ideally will move the positions from the Order class to here
    def get_one_position(self, symbol: str):
        """Get a position for a given symbol"""

    def get_all_positions(self):
        """Get all positions currently open"""
