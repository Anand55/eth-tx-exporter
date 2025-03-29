import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
BASE_URL = "https://api.etherscan.io/api"

def fetch_paginated_data(address, action, offset=1000, delay=0.05):
    """
    Fetch all pages of data for the given action.
    Stops when Etherscan returns an empty result.
    """
    page = 1
    while True:
        params = {
            "module": "account",
            "action": action,
            "address": address,
            "page": page,
            "offset": offset,
            "sort": "asc",
            "apikey": ETHERSCAN_API_KEY
        }

        try:
            print(f"📦 Fetching {action} page {page}...")
            response = requests.get(BASE_URL, params=params)
            data = response.json()

            if not data or "result" not in data or not data["result"]:
                print(f"🛑 {action} page {page} returned no data. Stopping.")
                break

            yield from data["result"]
            page += 1
            time.sleep(delay)

        except Exception as e:
            print(f"❌ Error on {action} page {page}: {e}")
            break

# Clean wrappers
def fetch_normal_transactions(address, offset=1000, delay=0.05):
    return fetch_paginated_data(address, "txlist", offset, delay)

def fetch_internal_transactions(address, offset=1000, delay=0.05):
    return fetch_paginated_data(address, "txlistinternal", offset, delay)

def fetch_erc20_transfers(address, offset=1000, delay=0.05):
    return fetch_paginated_data(address, "tokentx", offset, delay)

def fetch_erc721_transfers(address, offset=1000, delay=0.05):
    return fetch_paginated_data(address, "tokennfttx", offset, delay)
