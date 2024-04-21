import os
import sys
from apexpro.http_private_stark_key_sign import HttpPrivateStark
from apexpro.constants import (
    APEX_HTTP_TEST,
    NETWORKID_TEST,
)

# Paths required by ApexPro API
root_path = os.path.abspath(__file__)
root_path = "/".join(root_path.split("/")[:-2])
sys.path.append(root_path)


def apexpro_setup():
    client = HttpPrivateStark(
        APEX_HTTP_TEST,
        network_id=NETWORKID_TEST,
        stark_public_key=os.getenv("STARK_PUBLIC_KEY"),
        stark_private_key=os.getenv("STARK_PRIVATE_KEY"),
        stark_public_key_y_coordinate=os.getenv("STARK_PUBLIC_KEY_Y_COORDINATE"),
        api_key_credentials={
            "key": os.getenv("APEX_API_KEY"),
            "secret": os.getenv("APEX_API_SECRET"),
            "passphrase": os.getenv("APEX_API_PASSPHRASE"),
        },
    )
    return client


def get_apexpro_naming_convention(symbol):
    return symbol + "-USDC"
