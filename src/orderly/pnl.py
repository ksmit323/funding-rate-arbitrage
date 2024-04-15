import base64
from datetime import datetime
import json
import math

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from eth_account import Account, messages
from requests import Request, Session

from config import Config
from eip712 import MESSAGE_TYPES, get_on_chain_domain
from signer import Signer
from util import encode_key


class PnL(object):
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

    def settle_nonce(self) -> str:
        req = self._signer.sign_request(
            Request("GET", "%s/v1/settle_nonce" % self._config.base_url)
        )
        res = self._session.send(req)
        response = json.loads(res.text)
        print("settle_nonce:", response)

        return response["data"]["settle_nonce"]

    def settle_pnl(self):
        nonce = self.settle_nonce()

        d = datetime.utcnow()
        epoch = datetime(1970, 1, 1)
        timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

        register_message = {
            "brokerId": self._config.broker_id,
            "chainId": self._config.chain_id,
            "timestamp": timestamp,
            "settleNonce": nonce,
        }

        encoded_data = messages.encode_typed_data(
            domain_data=get_on_chain_domain(self._config.chain_id),
            message_types={"SettlePnl": MESSAGE_TYPES["SettlePnl"]},
            message_data=register_message,
        )
        signed_message = self._account.sign_message(encoded_data)

        req = self._signer.sign_request(
            Request(
                "POST",
                "%s/v1/settle_pnl" % self._config.base_url,
                json={
                    "message": register_message,
                    "signature": signed_message.signature.hex(),
                    "userAddress": self._account.address,
                    "verifyingContract": get_on_chain_domain(self._config.chain_id)[
                        "verifyingContract"
                    ],
                },
            )
        )
        res = self._session.send(req)
        response = json.loads(res.text)
        return response
