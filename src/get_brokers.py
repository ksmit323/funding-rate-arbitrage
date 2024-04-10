import requests

url = "https://api-evm.orderly.org/v1/public/broker/name"

response = requests.request("GET", url)

print(response.text)

"""
{"success":true,"data":{"rows":[
    {"broker_id":"woofi_pro","broker_name":"WOOFi Pro"},
    {"broker_id":"orderly","broker_name":"Orderly"},
    {"broker_id":"0xfin","broker_name":"0xfin"},
    {"broker_id":"busywhale","broker_name":"BusyWhale"},
    {"broker_id":"logx","broker_name":"LogX Aggregator "},
    {"broker_id":"emdx_dex","broker_name":"EMDX"},
    {"broker_id":"bitoro_network","broker_name":"Bitoro Network"},
    {"broker_id":"quick_perps","broker_name":"QuickSwap"},
    {"broker_id":"empyreal","broker_name":"Empyreal"},
    {"broker_id":"ibx","broker_name":"IBX"},
    {"broker_id":"ascendex","broker_name":"AscendEX"}]},
    "timestamp":1712567464497}
"""
