# import os
# import sys
# import time

# root_path = os.path.abspath(__file__)
# root_path = "/".join(root_path.split("/")[:-2])
# sys.path.append(root_path)


# from apexpro.constants import APEX_HTTP_TEST, APEX_HTTP_MAIN
# from apexpro.http_public import HttpPublic
# from apexpro.constants import APEX_WS_TEST
# from apexpro.websocket_api import WebSocket

# # print("Hello, Apexpro")

# client = HttpPublic(APEX_HTTP_TEST)
# # print(client.depth(symbol="BTC-USDC"))
# # print(client.ticker(symbol="BTC-USDC"))

# current_time = time.time()

# ws = f"wss://quote-testnet.pro.apex.exchange/realtime_public?v=2&timestamp={current_time}"

# # Connect with authentication!
# ws_client = WebSocket(
#     endpoint=ws,
# )

# print(ws_client.all_ticker_stream)

# # tickers = ws_client.send('{"op":"subscribe","args":["instrumentInfo.all"]}')
# # print(tickers)

# from apexpro.constants import APEX_WS_TEST
# from apexpro.websocket_api import WebSocket
# import time

# # Connect with authentication!
# ws_client = WebSocket(
#     endpoint=APEX_WS_TEST,
# )

# def h1(message):
#     global received_message
#     received_message = message

# ws_client.all_ticker_stream(h1)
# time.sleep(1) # Wait for ws connection

# print(received_message)

from order import ApexProOrder
from apex_utils import apexpro_setup

client = apexpro_setup()
order = ApexProOrder(client)
# print(order.create_market_order("ETH", 0.01, "BUY"))
# print(order.market_close_an_asset("ETH"))