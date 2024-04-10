from base64 import urlsafe_b64encode
from datetime import datetime
import json
import math
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from requests import PreparedRequest, Request
import urllib

from util import encode_key


class Signer(object):
    def __init__(
        self,
        account_id: str = None,
        key_pair: Ed25519PrivateKey = None,
    ) -> None:
        self._account_id = account_id
        self._key_pair = key_pair

    def sign_request(self, req: Request) -> PreparedRequest:
        d = datetime.utcnow()
        epoch = datetime(1970, 1, 1)
        timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

        json_str = ""
        if req.json is not None:
            json_str = json.dumps(req.json)

        url = urllib.parse.urlparse(req.url)
        message = str(timestamp) + req.method + url.path + json_str
        if len(url.query) > 0:
            message += "?" + url.query

        orderly_signature = urlsafe_b64encode(
            self._key_pair.sign(message.encode())
        ).decode("utf-8")

        req.headers = {
            "orderly-timestamp": str(timestamp),
            "orderly-account-id": self._account_id,
            "orderly-key": encode_key(self._key_pair.public_key().public_bytes_raw()),
            "orderly-signature": orderly_signature,
        }
        if req.method == "GET":
            req.headers["Content-Type"] = "application/x-www-form-urlencoded"
        elif req.method == "POST":
            req.headers["Content-Type"] = "application/json"

        return req.prepare()
