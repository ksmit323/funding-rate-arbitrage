from datetime import datetime
import math
from eth_account import Account as EthAccount, messages
import json
from requests import Request, Session

from config import Config
from eip712 import MESSAGE_TYPES, get_on_chain_domain
from signer import Signer


class Account(object):
    def __init__(
        self,
        config: Config,
        session: Session,
        signer: Signer,
        account: EthAccount,
    ) -> None:
        self._config = config
        self._session = session
        self._signer = signer
        self._account = account

    def get_client_holding(self):
        req = self._signer.sign_request(
            Request("GET", "%s/v1/client/holding" % self._config.base_url)
        )
        res = self._session.send(req)
        response = json.loads(res.text)
        # print("get_client_holding:", response)

        return response["data"]["holding"]

    def get_withdraw_nonce(self):
        req = self._signer.sign_request(
            Request("GET", "%s/v1/withdraw_nonce" % self._config.base_url)
        )
        res = self._session.send(req)
        response = json.loads(res.text)
        return response["data"]["withdraw_nonce"]

    def withdraw(self, token: str, amount: str):
        nonce = self.get_withdraw_nonce()

        d = datetime.utcnow()
        epoch = datetime(1970, 1, 1)
        timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

        withdraw_message = {
            "brokerId": self._config.broker_id,
            "chainId": self._config.chain_id,
            "receiver": self._account.address,
            "token": token,
            "amount": amount,
            "timestamp": timestamp,
            "withdrawNonce": nonce,
        }

        encoded_data = messages.encode_typed_data(
            domain_data=get_on_chain_domain(self._config.chain_id),
            message_types={"Withdraw": MESSAGE_TYPES["Withdraw"]},
            message_data=withdraw_message,
        )
        signed_message = self._account.sign_message(encoded_data)

        req = self._signer.sign_request(
            Request(
                "POST",
                "%s/v1/withdraw_request" % self._config.base_url,
                json={
                    "message": withdraw_message,
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
