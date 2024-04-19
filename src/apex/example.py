import os
import sys

root_path = os.path.abspath(__file__)
root_path = "/".join(root_path.split("/")[:-2])
sys.path.append(root_path)


from apexpro.constants import APEX_HTTP_TEST, APEX_HTTP_MAIN
from apexpro.http_public import HttpPublic

# print("Hello, Apexpro")

# client = HttpPublic(APEX_HTTP_TEST)
# print(client.depth(symbol="BTC-USDC"))
