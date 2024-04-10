from datetime import datetime
import json
import math
import requests

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from eth_account import Account, messages
from config import Config

from eip712 import MESSAGE_TYPES, get_off_chain_domain
from util import encode_key


class Register(object):
    def __init__(
        self,
        config: Config,
        account: Account,
    ) -> None:
        self._config = config
        self._account = account

    def register_account(self) -> str:
        res = requests.get("%s/v1/registration_nonce" % self._config.base_url)
        response = json.loads(res.text)
        registration_nonce = response["data"]["registration_nonce"]

        d = datetime.utcnow()
        epoch = datetime(1970, 1, 1)
        timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

        register_message = {
            "brokerId": self._config.broker_id,
            "chainId": self._config.chain_id,
            "timestamp": timestamp,
            "registrationNonce": registration_nonce,
        }

        encoded_data = messages.encode_typed_data(
            domain_data=get_off_chain_domain(self._config.chain_id),
            message_types={"Registration": MESSAGE_TYPES["Registration"]},
            message_data=register_message,
        )
        signed_message = self._account.sign_message(encoded_data)

        res = requests.post(
            "%s/v1/register_account" % self._config.base_url,
            headers={"Content-Type": "application/json"},
            json={
                "message": register_message,
                "signature": signed_message.signature.hex(),
                "userAddress": self._account.address,
            },
        )
        response = json.loads(res.text)
        print("register_account:", response)

        return response["data"]["account_id"]

    def add_access_key(self) -> Ed25519PrivateKey:
        orderly_key = Ed25519PrivateKey.generate()

        d = datetime.utcnow()
        epoch = datetime(1970, 1, 1)
        timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

        add_key_message = {
            "brokerId": self._config.broker_id,
            "chainId": self._config.chain_id,
            "orderlyKey": encode_key(orderly_key.public_key().public_bytes_raw()),
            "scope": "read,trading",
            "timestamp": timestamp,
            "expiration": timestamp + 1_000 * 60 * 60 * 24 * 365,  # 1 year
        }

        encoded_data = messages.encode_typed_data(
            domain_data=get_off_chain_domain(self._config.chain_id),
            message_types={"AddOrderlyKey": MESSAGE_TYPES["AddOrderlyKey"]},
            message_data=add_key_message,
        )
        signed_message = self._account.sign_message(encoded_data)

        res = requests.post(
            "%s/v1/orderly_key" % self._config.base_url,
            headers={"Content-Type": "application/json"},
            json={
                "message": add_key_message,
                "signature": signed_message.signature.hex(),
                "userAddress": self._account.address,
            },
        )
        response = json.loads(res.text)
        print("add_access_key:", response)

        return orderly_key
