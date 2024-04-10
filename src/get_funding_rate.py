# FUNDING RATE

import requests

def get_funding_rate():

    url = "https://api-evm.orderly.org/v1/public/funding_rate_history"

    querystring = {
        "symbol": "PERP_BTC_USDC",
        # "start_t": "1712304000000",
        # "end_t": "1712332800000",
        "page": "1"
    }

    response = requests.request("GET", url, params=querystring)

    print(response.text)



get_funding_rate()
