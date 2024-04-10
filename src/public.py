import json
import requests

from config import Config


class Public(object):
    def __init__(
        self,
        config: Config,
    ) -> None:
        self._config = config

    def get_symbols(self):
        res = requests.get("%s/v1/public/info" % self._config.base_url)
        response = json.loads(res.text)
        return response["data"]["rows"]
